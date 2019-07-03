// this file handles the chat chat messages

$(function() {
    // When we're using HTTPS, use WSS too.
    $('#all_messages').scrollTop($('#all_messages')[0].scrollHeight);
    var to_focus = $("#message");
    // Establish a ReconnectingWebSocket connection to the /ws/ endpoint.
    // Like http and https, websocket connections can be either ws or wss
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws/");

    chatsock.onmessage = function(message) {

        if($("#no_messages").length){
            $("#no_messages").remove();
        }
    // Convert the chat message text that the user submits into json format and send it to the server
        var data = JSON.parse(message.data);
        // When the server sends a presence payload containing an updated list of active users along with a lurkers count.
        // The javascript uses this data to update the users list and lurkers count.
        if(data.type == "presence"){
            //update lurkers count
            lurkers = data.payload.lurkers;
            lurkers_ele = document.getElementById("lurkers-count");
            lurkers_ele.innerText = lurkers;

            //update logged in users list
            user_list = data.payload.members;
            document.getElementById("loggedin-users-count").innerText = user_list.length;
            user_list_obj = document.getElementById("user-list");
            user_list_obj.innerText = "";

            //alert(user_list);
            for(var i = 0; i < user_list.length; i++ ){
                var user_ele = document.createElement('li');
                user_ele.setAttribute('class', 'list-group-item');
                user_ele.innerText = user_list[i];
                user_list_obj.append(user_ele);
            }

            return;
        }
        var chat = $("#chat")
        var ele = $('<li class="list-group-item"></li>')

        ele.append(
            '<strong>'+data.user+'</strong> : ')

        ele.append(
            data.message)

        chat.append(ele)
        $('#all_messages').scrollTop($('#all_messages')[0].scrollHeight);
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            message: $('#message').val()
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });

    setInterval(function() {
    chatsock.send(JSON.stringify("heartbeat"));
    }, 10000);
});

