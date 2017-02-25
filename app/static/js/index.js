function changeintoshort() {
    var text = document.getElementsByName('input_url')[0].value;
    if (text == null) {

    } else {
        $.ajax({
                url: '/change',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({'url': text}),
                contentType: 'application/json',
                success: function (data) {
                    if (data.success == true) {
                        var short_url = data.data.url;

                        document.getElementsByName('output_url')[0].innerText = short_url;

                    } else {
                        alert('转换失败');
                        document.getElementsByName('output_url')[0].innerText = '';
                    }

                }
            }
        )
    }

}