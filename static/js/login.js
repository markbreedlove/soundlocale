
function main(config) {
    $('#go').on('click', function() {
        $.ajax({
            url: config.baseUrl + 'session.json',
            type: 'post',
            data: {
                email: $('#email').val().trim(),
                password: $('#password').val()
            },
            success: function() {
                window.location = '/';
            },
            error: function(xhr, status, message) {
                alert(message);
            }
        });
    });
}

