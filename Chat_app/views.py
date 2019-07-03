from django.views import generic
from .models import ChatMessage
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404


def get_chat_fun():
    # We want to show the last 10 messages, ordered most-recent-last
    chat_queryset = ChatMessage.objects.all()  # order massage decended
    chat_message_count = len(chat_queryset)
    if chat_message_count > 0:
        first_message_id = chat_queryset[len(chat_queryset) - 1].id  # beacuase order by decended
    else:
        first_message_id = -1
    previous_id = -1
    if first_message_id != -1:
        try:
            previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
        except IndexError:
            previous_id = -1
    chat_messages =chat_queryset
    data = {
        'chat_messages': chat_messages,
        'first_message_id': previous_id,
    }

    return chat_messages , previous_id


class IndexView(generic.View):
    def get(self, request):
        # We want to show the last 10 messages, ordered most-recent-last
        chat_queryset = ChatMessage.objects.order_by("-created")[:10] # order massage decended
        chat_message_count = len(chat_queryset)
        if chat_message_count > 0:
            first_message_id = chat_queryset[len(chat_queryset) - 1].id # beacuase order by decended
        else:
            first_message_id = -1
        previous_id = -1
        if first_message_id != -1:
            try:
                previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
            except IndexError:
                previous_id = -1
        chat_messages = reversed(chat_queryset)
        data =  {
            'chat_messages': chat_messages,
            'first_message_id': previous_id,
        }

        return render(request, "chatdemo/chatroom.html", {
            'chat_messages': chat_messages,
            'first_message_id': previous_id,
        })



