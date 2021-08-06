const timer = new Timer();

timer.addEventListener('secondTenthsUpdated', function (e) {
    let timeValues = timer.getTimeValues();
    $('#chrono label').html(timeValues.toString(['hours', 'minutes', 'seconds']) + '.' + timeValues.secondTenths);
});

timer.addEventListener('started', function (e) {
    $('#chrono label').html(timer.getTimeValues().toString(['hours', 'minutes', 'seconds', 'secondTenths']));
});

timer.addEventListener('reset', function (e) {
    $('#chrono .values').html(timer.getTimeValues().toString());
});


function activate_order_mask_and_validation() {
    let input = document.getElementById('order');
    let maskOptions = {
        mask: '00-0000',
    };
    let mask = IMask(input, maskOptions);

    function valid_control() {
        if (mask.masked.isComplete) {
            input.className = 'form-control is-valid';
        } else {
            input.className = 'form-control is-invalid';
        }
    }

    valid_control()

    // 'accept' event fired on input when mask value has changed
    function log() {
        // console.log('value', mask.value)
        // console.log('unmaskedValue', mask.unmaskedValue)
        // console.log('typedValue', mask.typedValue)
        // console.log('isComplete', mask.masked.isComplete) true if input is valid
        // console.log('-------------------')
        valid_control()
    };
    mask.on("accept", log);

    // 'complete' event fired when the value is completely filled
    // Note: this makes sense only for Pattern-based masks
    // mask.on("complete", function () {console.log(mask.value)});
}


function activate_jobnote_mask_and_validation() {
    let input = document.getElementById('jobnote');
    let maskOptions = {
        mask: /^.+$/,
    };
    let mask = IMask(input, maskOptions);

    function valid_control() {
        if (mask.typedValue.length > 10) {
            input.className = 'form-control is-valid';
        } else {
            input.className = 'form-control is-invalid';
        }
    }

    mask.on("accept", function () {
        valid_control()
    });
    valid_control()
}


function activate_manager_mask_and_validation() {
    let input = $('#sel-manager')

    function valid_control() {
        if (input.val() === '0') {
            input[0].className = 'form-control is-invalid';
        } else {
            input[0].className = 'form-control is-valid';
        }
    }

    function fillDataList(optionList) {
        let container = document.getElementById('datalistOptions');
        let str=''; // variable to store the options

        for (var i=0; i < optionList.length;++i){
            str += '<option value="'+optionList[i]+'" />'; // Storing options in variable
            // example <option value="{{ manager.id }}"> {{ manager.name }} </option>
        }

        $('#count .badge').text(i)
        container.innerHTML = str
    }

    function get_latest_jobnotes() {
        $.ajax({
            url: '/get_latest_jobnotes/',
            dataType: 'json',
            data: {managerid: input.val()},
            success: function (data) {
                console.log('«GET JOBNOTES» RETURNED DATA:', data['error'])
                if (data['error'] === 'all ok') {
                    let latest_jobnotes = JSON.parse(data['latest_jobnotes']);
                    fillDataList(latest_jobnotes)
                }
            }
        })
    }

    input.on('change', function () {
        valid_control()
        get_latest_jobnotes()
    });
    valid_control()
}


function set_state_running(sec, restoring) {
    timer.start({precision: 'secondTenths', startValues: {seconds: sec}})

    if (restoring) {
        if (restoring.order !== null) {
            console.log('activate first tab...')
            let sel = document.querySelector('#nav-tab-order')
            bootstrap.Tab.getOrCreateInstance(sel).show()
            document.getElementById('order').value=restoring.order
            document.getElementById('radio-'+restoring.jobtype).checked=true
            activate_order_mask_and_validation()
        } else {
            console.log('activate second tab...')
            let sel = document.querySelector('#nav-tab-manager')
            bootstrap.Tab.getOrCreateInstance(sel).show()
            document.getElementById('sel-manager').value=restoring.managerid
            document.getElementById('jobnote').value=restoring.jobnote
            document.getElementById('radio-'+restoring.jobtype).checked=true
            activate_jobnote_mask_and_validation()
            activate_manager_mask_and_validation()
        }
    }

    $('#nav-tab-order').prop('disabled', true);
    $('#nav-tab-manager').prop('disabled', true);

    $('#order').prop('disabled', true);
    $('#sel-manager').prop('disabled', true);
    $('#jobnote').prop('disabled', true);

    $('.form-check-input').prop('disabled', true);
    $('#startButton').prop('disabled', true);
    $('#stopButton').prop('disabled', false);
    $('#cancelButton').prop('disabled', false);
}


function set_state_stopped() {
    timer.stop();

    $('#nav-tab-order').prop('disabled', false);
    $('#nav-tab-manager').prop('disabled', false);

    $('#order').prop('disabled', false);
    $('#sel-manager').prop('disabled', false);
    $('#jobnote').prop('disabled', false);

    $('.form-check-input').prop('disabled', false);
    $('#startButton').prop('disabled', false);
    $('#stopButton').prop('disabled', true);
    $('#cancelButton').prop('disabled', true);
}


function restore_on_reload() {
    // TODO нужно возвращать номер заказа, манагера и дескрипшн
    if (duration) {
        // сюда попадаем, если юзер включил таймер и перезагрузил страницу. Django возвращает в переменной
        // duration, сколько прошоло времени с запуска
        console.log('restoring order:', restoring.order)
        console.log('restoring manager:', restoring.manager)
        console.log('restoring jobnote:', restoring.jobnote)
        console.log('restoring jobtype:', restoring.jobtype)

        let seconds = parseInt(duration)
        set_state_running(seconds, restoring)
    } else {
        set_state_stopped()
    }
}


$(document).ready(function () {
    activate_order_mask_and_validation()
    activate_manager_mask_and_validation()
    activate_jobnote_mask_and_validation()
    restore_on_reload()

    $('#startButton').on('click', function () {
        let active_tab = document.querySelectorAll('#nav-tab button[aria-selected="true"]')[0].id
        let valid_order = document.getElementById('order').classList.contains('is-valid')
        let valid_manager = document.getElementById('sel-manager').classList.contains('is-valid')
        let valid_jobnote = document.getElementById('jobnote').classList.contains('is-valid')

        let data = {}
        data['active_tab'] = active_tab
        data['jobtype'] = $('input[name="jobRadio"]:checked').val();

        function doajax() {
            $.ajax({
                url: '/click_start/',
                data: data,
                dataType: 'json',
                success: function (answer) {
                    console.log('«START» RETURNED DATA:', answer['error'])
                    if (answer['error'] === 'all ok') {
                        set_state_running(0, null)
                    }
                }
            })
        }

        if (active_tab === 'nav-tab-order' && valid_order) {
            data['order'] = $('#order').val()
            doajax()
        } else if (active_tab === 'nav-tab-manager' && valid_manager && valid_jobnote) {
            data['managerid'] = $('#sel-manager').val()
            data['jobnote'] = $('#jobnote').val()
            doajax()
        } else {
            console.log('Input invalidate!')
            // нужно выяснить, на какой мы вкладке, и потом передевать фокус
            // document.getElementById("order").focus();
        }
    });

    $('#stopButton').on('click', function () {
        let active_tab = document.querySelectorAll('#nav-tab button[aria-selected="true"]')[0].id
        let valid_order = document.getElementById('order').classList.contains('is-valid')
        let valid_manager = document.getElementById('sel-manager').classList.contains('is-valid')
        let valid_jobnote = document.getElementById('jobnote').classList.contains('is-valid')

        let data = {}
        data['active_tab'] = active_tab
        data['jobtype'] = $('input[name="jobRadio"]:checked').val();

        if (active_tab === 'nav-tab-order' && valid_order) {
            data['order'] = $('#order').val()
        } else if (active_tab === 'nav-tab-manager' && valid_manager && valid_jobnote) {
            data['managerid'] = $('#sel-manager').val()
            data['jobnote'] = $('#jobnote').val()
        } else {
            console.log('Input invalidate!')
            // нужно выяснить, на какой мы вкладке, и потом передевать фокус
            // document.getElementById("order").focus();
        }

        $.ajax({
            url: '/click_stop/',
            data: data,
            dataType: 'json',
            success: function (answer) {
                console.log('«STOP» RETURNED DATA:', answer['error'])
                if (answer['error'] === 'all ok') {
                    set_state_stopped();
                }
            }
        })
    });

    $('#cancelButton').on('click', function () {
        if (timer.isRunning) {
            $.ajax({
                url: '/click_cancel/',  // удаляем из базы последнюю запись 'start'
                success: function (answer) {
                    console.log('«CANCEL» RETURNED DATA:', answer['error'])
                }
            })
        }
        set_state_stopped()
        $('#chrono label').html(timer.getTimeValues().toString());
    });

});