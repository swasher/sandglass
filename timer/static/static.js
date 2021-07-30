const timer = new Timer();

timer.addEventListener('secondTenthsUpdated', function (e) {
    let timeValues = timer.getTimeValues();
    $('#chrono label').html(timeValues.toString(['hours','minutes', 'seconds']) + '.' + timeValues.secondTenths);
});

timer.addEventListener('started', function (e) {
    $('#chrono label').html(timer.getTimeValues().toString(['hours', 'minutes', 'seconds', 'secondTenths']));
});

timer.addEventListener('reset', function (e) {
    $('#chrono .values').html(timer.getTimeValues().toString());
});


function activate_order_mask_and_validation () {
    let input = document.getElementById('order');
    let maskOptions = {
        mask: '00-0000',
    };
    let mask = IMask(input, maskOptions);

    function valid_control () {
        if (mask.masked.isComplete) {
            input.className = 'form-control is-valid';
        } else {
            input.className = 'form-control is-invalid';
        }
    }
    valid_control()

    // 'accept' event fired on input when mask value has changed
    function log () {
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


function activate_jobnote_mask_and_validation () {
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
    valid_control()

    mask.on("accept", function (){valid_control()});
}


function activate_manager_mask_and_validation () {
    let input = document.getElementById('sel-manager');
    let maskOptions = {
        mask: /^.+$/,
    };
    let mask = IMask(input, maskOptions);

    function valid_control() {
        let optionFound = false,
            datalist = input['list'];
        // Определение, существует ли option с текущим значением input.
        for (let j = 0; j < datalist.options.length; j++) {
            if (mask.unmaskedValue === datalist.options[j].value) {
                optionFound = true;
                break;
            }
        }
        // используйте функцию setCustomValidity API проверки ограничений валидации
        // чтобы обеспечить ответ пользователю, если нужное значение в datalist отсутствует
        if (optionFound) {
          input.className = 'form-control is-valid';
        } else {
          input.className = 'form-control is-invalid';
        }
    }
    valid_control()

    mask.on("accept", function (){valid_control()});
}



function set_state_running(tab, sec) {
    timer.start({precision: 'secondTenths', startValues: {seconds: sec}})
    $('#startButton').prop('disabled', true);
    $('#stopButton').prop('disabled', false);
    $('#cancelButton').prop('disabled', false);
    $('#order').prop('disabled', true);
    $('#jobnote').prop('disabled', true);
    $('#zakaz-tab').prop('disabled', true);
    $('#managers-tab').prop('disabled', true);
    $('.form-check-input').prop('disabled', true);
}


function set_state_stopped() {
    timer.stop();
    $('#startButton').prop('disabled', false);
    $('#stopButton').prop('disabled', true);
    $('#cancelButton').prop('disabled', true);
    $('#order').prop('disabled', false);
    $('#jobnote').prop('disabled', false);
    $('#zakaz-tab').prop('disabled', false);
    $('#managers-tab').prop('disabled', false);
    $('.form-check-input').prop('disabled', false);
}


function restore_on_reload() {
    // TODO нужно возвращать номер заказа, манагера и дескрипшн
    if (duration) {
        // сюда попадаем, если юзер включил таймер и перезагрузил страницу. Django возвращает в переменной
        // duration, сколько прошоло времени с запуска
        let seconds = parseInt(duration)
        set_state_running('tab', seconds)
    } else {
        set_state_stopped()
    }
}


$(document).ready(function() {
    activate_order_mask_and_validation()
    activate_manager_mask_and_validation()
    activate_jobnote_mask_and_validation()
    restore_on_reload()

    $('#startButton').on('click', function () {
        let active_tab = $("ul#myTab button.active")[0].id
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
                success: function (data) {
                    console.log('«START» RETURNED DATA:', data['error'])
                    if (data['error'] === 'all ok') {
                        set_state_running('tab', 0)
                    }
                }
            })
        }

        if (active_tab === 'order-tab' && valid_order) {
            data['order'] = $('#order').val()
            doajax()
        }
        else if (active_tab === 'managers-tab' && valid_manager && valid_jobnote) {
            data['managerid'] = $('#datalistOptions option[value=' + $('#sel-manager').val() + ']').attr('id')
            data['jobnote'] = $('#jobnote').val()
            doajax()
        }
        else {
            console.log('Input invalidate!')
            // нужно выяснить, на какой мы вкладке, и потом передевать фокус
            // document.getElementById("order").focus();
        }
    });

    $('#stopButton').on('click', function () {
        let active_tab = $("ul#myTab button.active")[0].id
        let valid_order = document.getElementById('order').classList.contains('is-valid')
        let valid_manager = document.getElementById('sel-manager').classList.contains('is-valid')
        let valid_jobnote = document.getElementById('jobnote').classList.contains('is-valid')

        let data = {}
        data['active_tab'] = active_tab
        data['jobtype'] = $('input[name="jobRadio"]:checked').val();

        if (active_tab === 'order-tab' && valid_order) {
            data['order'] = $('#order').val()
        }
        else if (active_tab === 'managers-tab' && valid_manager && valid_jobnote) {
            data['managerid'] = $('#datalistOptions option[value=' + $('#sel-manager').val() + ']').attr('id')
            data['jobnote'] = $('#jobnote').val()
        }
        else {
            console.log('Input invalidate!')
            // нужно выяснить, на какой мы вкладке, и потом передевать фокус
            // document.getElementById("order").focus();
        }

        $.ajax({
            url: '/click_stop/',
            data: data,
            dataType: 'json',
            success: function (data) {
                console.log('«STOP» RETURNED DATA:', data['error'])
                if (data['error'] === 'all ok') {
                    set_state_stopped();
                }
            }
        })
    });

    $('#cancelButton').on('click', function () {
        if (timer.isRunning) {
            $.ajax({
                url: '/click_cancel/',  // удаляем из базы последнюю запись 'start'
                success: function (data) {
                    console.log('«CANCEL» RETURNED DATA:', data['error'])
                }
            })
        }
        set_state_stopped()
    });

});