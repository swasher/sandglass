let timer = new Timer();


$('#stopButton').click(function () {
    timer.stop();
});

timer.addEventListener('secondTenthsUpdated', function (e) {
    $('#chrono label').html(timer.getTimeValues().toString(['hours', 'minutes', 'seconds', 'secondTenths']));
});

timer.addEventListener('started', function (e) {
    $('#chrono label').html(timer.getTimeValues().toString(['hours', 'minutes', 'seconds', 'secondTenths']));
});

timer.addEventListener('reset', function (e) {
    $('#chrono .values').html(timer.getTimeValues().toString());
});


$(document).ready(function() {
    // var data = JSON.parse("{{data|escapejs}}");
    console.log('DURATION', "{{duration}}")

    $('#stopButtonZ').prop('disabled', true);
    $('#stopButtonM').prop('disabled', true);

    let order_input = document.getElementById('order');
    let maskOptions = {
      mask: '00-0000'
    };
    let mask = IMask(order_input, maskOptions);

    $('#startButtonZ').on('click', function () {
        if (document.getElementById('order').classList.contains('is-valid')) {

            timer.start({precision: 'secondTenths'});
            $('#order').prop('disabled', true);
            $('#startButtonZ').prop('disabled', true);
            $('#stopButtonZ').prop('disabled', false);
            $('#managers-tab').prop('disabled', true);
            $('.form-check-input').prop('disabled', true);

            let order = $('#order').val()
            let jobtype = $('input[name="jobRadio"]:checked').val();

            $.ajax({
                url: '/click_startz/',
                data: {order: order, jobtype: jobtype},
                dataType: 'json',
                success: function (data) {
                    console.log('«START» RETURNED DATA:', data['error'])
                }
            })

        } else {
            console.log('INVALID!')
            document.getElementById("order").focus();
        }

    });

    $('#stopButtonZ').on('click', function () {

        timer.stop();
        $('#order').prop('disabled', false);
        $('#startButtonZ').prop('disabled', false);
        $('#stopButtonZ').prop('disabled', true);
        $('#managers-tab').prop('disabled', false);
        $('.form-check-input').prop('disabled', false);

        let order = $('#order').val()
        let jobtype = $('input[name="jobRadio"]:checked').val();
        console.log('Order: ', order, 'Jobtype:', jobtype)

        $.ajax({
            url: '/click_stopz/',
            data: {order: order, jobtype: jobtype},
            dataType: 'json',
            success: function (data) {
                console.log('«STOP» RETURNED DATA:', data['error'])
            }
        })
    });

});