$(function () {
    $.ajax({
            url: '/login_status',
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data.success == true) {
                    window.location.href = '../../admin'
                }
            }
        }
    )

})

function login() {
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;
    if (name != null && password != null) {
        $.ajax({
                url: '/login',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({'name': name, 'password': password}),
                contentType: 'application/json',
                success: function (data) {
                    if (data.success == true) {
                        window.location.href = '../../admin'
                    }

                }
            }
        )

    }

}