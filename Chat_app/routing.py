from channels import route
import channels
from django.urls import reverse


# This function will display all messages received in the console
def message_handler(message):
    print(message['text'])


channel_routing = [
    route("websocket.receive", message_handler)  # we register our message handler
]