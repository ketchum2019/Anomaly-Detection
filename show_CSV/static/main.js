function post() {
        console.log("posting")
        var host = '127.0.0.1';
        var port = '8001';
        $.ajax({
            url: "deal_post/",
            type: "POST",
            data: {host: host, port: port},
            async: 'asynchronous',
            success: function (arg) {
                alert(data['host'])
            },
            error: function (error) {
                alert("error")
            }
        })
    }