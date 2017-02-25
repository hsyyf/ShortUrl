$(function () {
    $.ajax({
        url: '/profile',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            if (data.success == true) {
                var new_name = data.data.name;
                var name_div = document.getElementById('name');
                name_div.value = new_name;
            }
        }
    })

    $.ajax({
        url: '/black_list',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            if (data.success == true) {
                var url_list = data.data.url_list;
                var tbody = document.getElementById('black_list');
                for (black in url_list) {
                    var new_tr = document.createElement('tr');
                    new_tr.setAttribute('name', 'url');
                    new_tr.innerHTML = '<td>' + url_list[black] + '</td> <td><input name="SingleChoice" type="checkbox" value="' + url_list[black] + '" onclick="change_status()"/></td>';
                    tbody.appendChild(new_tr);
                }
            }
        }
    })
});

function updateData() {
    var name = document.getElementById('name').value;
    var old_password = document.getElementById('old_password').value;
    var password = document.getElementById('password').value;
    var confirm_password = document.getElementById('confirm_password').value;

    $.ajax({
        url: '/profile',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify({
            'name': name,
            'old_password': old_password,
            'password': password,
            'confirm_password': confirm_password
        }),
        contentType: 'application/json',
        success: function (data) {
            if (data.success == true) {
                //windows.location.href = "NEW_URL";
                alert('数据更新成功');
            } else {
                alert('数据更新失败');
            }

        }
    })

}

function add_Url() {
    var url = document.getElementById('black_url').value;
    $.ajax({
            url: '/add_url',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'url': url
            }),
            contentType: 'application/json',
            success: function (data) {
                if (data.success == true) {
                    $('#add_Modal').modal('hide');

                    var tbody = document.getElementById('black_list');
                    var new_tr = document.createElement('tr');
                    new_tr.setAttribute('name', 'url');
                    new_tr.innerHTML = '<td>' + url + '</td> <td><input name="SingleChoice" type="checkbox" value="' + url + '" onclick="change_status()"/></td>';
                    tbody.appendChild(new_tr);
                } else {
                    alert('数据添加失败');
                }
            }
        }
    )
}

function del_Url() {
    var all_checkbox = document.getElementsByName('SingleChoice');
    var url_list = [];
    for (checkbox in all_checkbox) {
        if (all_checkbox[checkbox].checked) {
            url_list.push(all_checkbox[checkbox].value);
        }
    }
    $.ajax(
        {
            url: '/del_url',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'url': url_list
            }),
            contentType: 'application/json',
            success: function (data) {
                $('tr[name=url]').remove();
                $.ajax({
                    url: '/black_list',
                    type: 'GET',
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function (data) {
                        if (data.success == true) {
                            var url_list = data.data.url_list;
                            var tbody = document.getElementById('black_list');
                            for (black in url_list) {
                                var new_tr = document.createElement('tr');
                                new_tr.setAttribute('name', 'url');
                                new_tr.innerHTML = '<td>' + url_list[black] + '</td> <td><input name="SingleChoice" type="checkbox" value="' + url_list[black] + '" onclick="change_status()"/></td>';
                                tbody.appendChild(new_tr);
                            }
                        }
                    }
                });

            }
        }
    )
    $("#del_url").attr({"disabled": "disabled"});
}

function AllChange() {
    var all_checkbox = document.getElementsByName('SingleChoice');
    var flag = document.getElementsByName('AllChoices')[0].checked;
    for (checkbox in all_checkbox) {
        all_checkbox[checkbox].checked = flag;
    }
    if (flag) {
        $("#del_url").removeAttr("disabled");
    } else {
        $("#del_url").attr({"disabled": "disabled"});
    }
}

function change_status() {
    var all_checkbox = document.getElementsByName('SingleChoice');
    var flag = false;
    for (checkbox in all_checkbox) {
        if (all_checkbox[checkbox].checked) {
            flag = true;
            break;
        }
    }

    if (flag) {
        $("#del_url").removeAttr("disabled");
    } else {
        $("#del_url").attr({"disabled": "disabled"});
    }
}

function logout() {
    $.ajax({
        url: '/logout',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            if (data.success == true) {
                window.location.href = '../../index'
            }

        }
    })

}