/**
 * Created by arch on 17-2-25.
 */

function install_app() {
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;
    var confirm_password = document.getElementById('confirm_password').value;
    var domain = document.getElementById('domain').value;

    $.ajax({
        url: '/install',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify({
            'name': name,
            'password': password,
            'confirm_password': confirm_password,
            'domain': domain
        }),
        contentType: 'application/json',
        success: function (data) {
            if (data.success == true) {
                window.location.href = '../../login'
            }

        }
    })

}
