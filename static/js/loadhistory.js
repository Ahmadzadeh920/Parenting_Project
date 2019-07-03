// this file handles loading the previous chat messages

$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

    var loadhistorysock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/loadhistory/");

    // When the server responds with the previous messages, the javascript updates the client side chat room with the historical chat messages

    loadhistorysock.onmessage = function(message) {

        var data = JSON.parse(message.data);

        new_messages = data.messages

        last_id = data.previous_id
        // If the server indicates that there are no more messages in the scrollback, the javascript removes the “Load old messages” button.
        if(last_id == -1){
            $("#load_old_messages").remove();
            $("#last_message_id").text(last_id)
            if(new_messages.length == 0){
                return;
            }
        }
        else{
            $("#last_message_id").text(last_id)
        }

        var chat = $("#chat")

        for(var i=new_messages.length - 1; i>=0; i--){
            var ele = $('<li class="list-group-item"></li>')

            ele.append(
                '<strong>'+new_messages[i]['user']+'</strong> : '
                )

            ele.append(
                new_messages[i]['message'])

            chat.prepend(ele)
        }

    };

    // When the user clicks on the “Load old messages” button, the javascript sends the last_message_id variable to the /loadhistory endpoint

    $("#load_old_messages").on("click", function(event) {
        var message = {
            last_message_id: $('#last_message_id').text()
        }
        loadhistorysock.send(JSON.stringify(message));
        return false;
    });
});
