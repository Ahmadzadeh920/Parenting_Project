from channels import Group
from channels.sessions import channel_session
from .models import ChatMessage
from django.contrib.auth.models import User
import json
from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils.html import escape
from django.core import serializers
import markdown
import re
from django.conf import settings
from django.urls import reverse
from channels_presence.models import Room
from channels_presence.decorators import touch_presence

from django.dispatch import receiver
from channels_presence.signals import presence_changed
from channels import Group
#______________________________________websocket connection
@channel_session_user_from_http
def chat_connect(message):
    # The reply_channel of the connection is added to the all group
    # when user A send massage , all of user connected in group receive this massage
    Group("all").add(message.reply_channel)
    # The connection is also added to the all room
    # This is used to keep track of the number of users connected to the chat room.
    Room.objects.add("all", message.reply_channel.name, message.user)
    # Finally the following response is sent to the user to confirm that the connection has been accepted
    message.reply_channel.send({"accept": True})

#____________________________________________
# is used to note the periodic beat sent from the users’ browser
# which ensures that users are not removed from the list of active users connected to the chat room
@touch_presence
@channel_session_user
def chat_receive(message):
    # Receive and decode the json message
    data = json.loads(message['text'])
    # Confirm that the json contains a message key which holds the content of the message
    if not data['message']:
        return
    # Confirm that the user is authenticated since it does not make sense to accept chat messages from unathenticated users
    if not message.user.is_authenticated:
        return
    # Escape the message using the escape function from django.utils.html
    # Escape maens spacial character convert to HTML code e.g. newline
    current_message = escape(data['message'])
    urlRegex = re.compile(
        u'(?isu)(\\b(?:https?://|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)[^\\s()<'
        u'>\\[\\]]+[^\\s`!()\\[\\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])'
    )

    processed_urls = list()
    # Check if the message contains any valid urls and convert the urls to links.
    #  Eg- https://google.com becomes <a href="https://google.com">https://google.com</a>
    for obj in urlRegex.finditer(current_message):
        old_url = obj.group(0)
        if old_url in processed_urls:
            continue
        processed_urls.append(old_url)
        new_url = old_url
        if not old_url.startswith(('http://', 'https://')):
            new_url = 'http://' + new_url
        new_url = '<a href="' + new_url + '">' + new_url + "</a>"
        current_message = current_message.replace(old_url, new_url)
    m = ChatMessage(user=message.user, message=data['message'], message_html=current_message)
    m.save()

    my_dict = {'user': m.user.username, 'message': current_message}
    Group("all").send({'text': json.dumps(my_dict)})

#______________________________-chat_disconnect

@channel_session_user
def chat_disconnect(message):
    Group("all").discard(message.reply_channel)
    Room.objects.remove("all", message.reply_channel.name)

#_______________________________________
#that sends the latest list of users and the count of anonymous users.
# This function is called everytime a user connects or disconnects from the chat room.
def broadcast_presence(sender, room, **kwargs):
    # Broadcast the new list of present users to the room.
    Group(room.channel_name).send({
        'text': json.dumps({
            'type': 'presence',
            'payload': {
                'channel_name': room.channel_name,
                # members : the list of logged in users connected to the chat room
                'members': [user.username for user in room.get_users()],
                # lurkers : an integer count representing how many anonymous users are connected to the chat
                'lurkers': int(room.get_anonymous_count()),
            }
        })
    })

#_____________________________

@channel_session_user_from_http
# just accepts the websocket connect by sends the standard response to indicate that the connection has been accepted
def loadhistory_connect(message):
    message.reply_channel.send({"accept": True})


@channel_session_user
#  disonnecting the connection, we don’t need to do anything.
def loadhistory_disconnect(message):
    pass

#_________________________________

@channel_session_user
def loadhistory_receive(message):
    data = json.loads(message['text'])
    # field__lookuptype which lookuptype=lte means lower value of value
    # which represents the chat message id before the last message that has been rendered in the chat room for the current user.
    chat_queryset = ChatMessage.objects.filter(id__lte=data['last_message_id']).order_by("-created")[:10]
    chat_message_count = len(chat_queryset)
    if chat_message_count > 0:
        first_message_id = chat_queryset[len(chat_queryset)-1].id
    else:
        first_message_id = -1
    previous_id = -1
    if first_message_id != -1:
        try:
            previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
        except IndexError:
            previous_id = -1

    chat_messages = reversed(chat_queryset)
    cleaned_chat_messages = list()
    for item in chat_messages:
        current_message = item.message_html
        cleaned_item = {'user' : item.user.username, 'message' : current_message }
        cleaned_chat_messages.append(cleaned_item)

    my_dict = { 'messages' : cleaned_chat_messages, 'previous_id' : previous_id }
    message.reply_channel.send({'text': json.dumps(my_dict)})