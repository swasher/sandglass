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


function update_job_info(order) {
    $.ajax({
        url: '/get_info/',
        dataType: 'json',
        data: {order: order},
        success: function (data) {
            console.log(data)
            console.log('«GET JOB INFO» RETURNED DATA:', data.error)
            if (data['error'] === 'ok') {
                console.log('jobname', data.jobname)
                console.log('manager_name', data.manager_name)
                console.log('manager_email', data.manager_email)
                $('#manager-name').text(data.manager_name)
                $('#job-name').text(data.jobname)
            }
        }
    })
}


function activate_order_mask_and_validation() {
    let input = document.getElementById('order');
    let maskOptions = {
        mask: '00-0000',
    };
    let mask = IMask(input, maskOptions);

    function valid_control() {
        if (mask.masked.isComplete) {
            input.className = 'form-control is-valid';
            // ========== Здесь мы вызываем функцию обновления данных о заказе
            update_job_info(mask.value)
        } else {
            input.className = 'form-control is-invalid';
        }
    }

    valid_control()

    function log() {
        console.log('value', mask.value)
        console.log('unmaskedValue', mask.unmaskedValue)
        console.log('typedValue', mask.typedValue)
        console.log('isComplete', mask.masked.isComplete)  // true if input is valid
        console.log('-------------------')
    };

    // 'accept' event fired on input when mask value has changed
    mask.on("accept", function () {
        valid_control()
        // log()
    });

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
        /*
        Заполняет выпадающий список `datalistOptions` списком его работ `optionList`.
        Вызывается из get_latest_jobnotes, при выборе менеджера.
         */
        let container = document.getElementById('datalistOptions');
        let str=''; // variable to store the options

        for (var i=0; i < optionList.length;++i){  // тут должен быть именно var i, чтобы i осталось видимым дальше.
            str += '<option value="'+optionList[i]+'" />';
            // example <option value="{{ manager.id }}"> {{ manager.name }} </option>
        }

        $('#count .badge').text(i)
        container.innerHTML = str
    }

    function get_latest_jobnotes() {
        /*
        Получает с сервера список работ менеджера за последние n дней.
        n захаркоджено во view.py в get_latest_jobnotes()
         */
        $.ajax({
            url: '/get_latest_jobnotes/',
            dataType: 'json',
            data: {managerid: input.val()},
            success: function (data) {
                console.log('«GET JOBNOTES» RETURNED DATA:', data['error'])
                if (data['error'] === 'ok') {
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
    /*
    Мы вызываем эту функцию в двух случаях - при нажатии кнопки Start (т.е. первый запуск, и при нажатии F5, т.е. когда
    нам нужно вернуть состояние всех полей. В первом случае в restroring вызывающая функция передает null, и содержимое
    полей мы не трогаем, только дизаблим
     */
    timer.start({precision: 'secondTenths', startValues: {seconds: sec}})

    if (restoring) {
        if (restoring.tab === 'first') {
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
    if (restoring.needed) {
        // сюда попадаем, если юзер включил таймер и перезагрузил страницу. Django возвращает в переменной
        // duration, сколько прошоло времени с запуска
        let seconds = parseInt(restoring.duration)

        console.log('restoring order:', restoring.order)
        console.log('restoring manager:', restoring.manager)
        console.log('restoring jobnote:', restoring.jobnote)
        console.log('restoring jobtype:', restoring.jobtype)
        console.log('restoring tab:', restoring.tab)
        console.log('restoring seconds:', seconds)

        set_state_running(seconds, restoring)
    } else {
        set_state_stopped()
    }
}


function time_difference() {
    /*
    Sample return:
        {
          "abbreviation": "MSK",
          "client_ip": "89.208.171.38",
          "datetime": "2021-08-30T11:32:40.761822+03:00",
          "day_of_week": 1,
          "day_of_year": 242,
          "dst": false,
          "dst_from": null,
          "dst_offset": 0,
          "dst_until": null,
          "raw_offset": 10800,
          "timezone": "Europe/Moscow",
          "unixtime": 1630312360,
          "utc_datetime": "2021-08-30T08:32:40.761822+00:00",
          "utc_offset": "+03:00",
          "week_number": 35
        }
     */
    fetch('http://worldtimeapi.org/api/timezone/Europe/Moscow')
        .then(res => res.json())
        .then((out) => {
            let internet_time = new Date(out.datetime)
            let computer_time = new Date();

            let difference = (computer_time-internet_time)/1000
            // console.log('Internet time: ', internet_time);
            // console.log('computer_time', computer_time)
            // console.log('difference, s', difference)
            // console.log('type computer_time', typeof computer_time)
            // console.log('type internet_time', typeof internet_time)
            $('#delta').text(difference+'s')
        }).catch(err => console.error(err));
}


$(document).ready(function () {
    activate_order_mask_and_validation()
    activate_manager_mask_and_validation()
    activate_jobnote_mask_and_validation()
    restore_on_reload()
    time_difference()


    $("#order").keydown(function (event) {
     if (event.which == 13) {
         event.preventDefault();
         $('#startButton').click();
         console.log('click event - lets start!');
     }
    });

    $("#jobnote").keydown(function (event) {
     if (event.which == 13) {
         event.preventDefault();
         $('#startButton').click();
         console.log('click event - lets start!');
     }
    });



    $('#startButton').on('click', function () {
        let active_tab = document.querySelectorAll('#nav-tab button[aria-selected="true"]')[0].id
        let valid_order = document.getElementById('order').classList.contains('is-valid')
        let valid_manager = document.getElementById('sel-manager').classList.contains('is-valid')
        let valid_jobnote = document.getElementById('jobnote').classList.contains('is-valid')

        let data = {}
        // deprecated 31.08.21
        // data['active_tab'] = active_tab
        data['jobtype'] = $('input[name="jobRadio"]:checked').val();

        function doajax(data) {
            $.ajax({
                url: '/click_start/',
                data: data,
                dataType: 'json',
                success: function (answer) {
                    console.log('«START» RETURNED DATA:', answer['error'])
                    if (answer['error'] === 'ok') {
                        set_state_running(0, null)
                    }
                }
            })
        }

        function add_date_to_jobnote(note) {
            /*
            Проверка, содержит ли УЖЕ строка дату.
            Если нет, добавляет дату в начале строки, иначе возвращает строку неизменно.
             */

            // Конструкция || [] возвращает пустой словарь вместо None, если совпад. не найдено, и у этого словаря длина - ноль.
            // containDate содержит 0, если в строке нет даты, и 1, если содержит
            let containDate = note.match(/^\d{4}-\w{3}-\d/)|| []

            if (!containDate.length) {
                let now = new Date();
                // date_string will be date as "2009-Feb-1"
                let date_string = now.getFullYear()+'-'+now.toLocaleString('en', { month: 'short' })+'-'+now.getDate();
                note = date_string + ' ' + note
            }
            return note
        }

        if (active_tab === 'nav-tab-order' && valid_order) {
            data['order'] = $('#order').val()
            data['is_order'] = true
            doajax(data)
        } else if (active_tab === 'nav-tab-manager' && valid_manager && valid_jobnote) {
            // add date to jobnote
            let noteField = $('#jobnote')
            let note = add_date_to_jobnote(noteField.val())
            noteField.val(note)
            data['jobnote'] = noteField.val()
            data['managerid'] = $('#sel-manager').val()
            data['is_order'] = false
            doajax(data)
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
            data['is_order'] = true
        } else if (active_tab === 'nav-tab-manager' && valid_manager && valid_jobnote) {
            data['managerid'] = $('#sel-manager').val()
            data['jobnote'] = $('#jobnote').val()
            data['is_order'] = false
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
                if (answer['error'] === 'ok') {
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