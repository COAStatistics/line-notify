from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from . import models

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
webhook = WebhookHandler(settings.CHANNEL_SECRET)

# Create your views here.

def home(request):
    if request.method == 'GET':
        return HttpResponse('Hello!')

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        print('line_bot_api channel access token = ' + settings.CHANNEL_ACCESS_TOKEN)
        print('webhook channel secret = ' + settings.CHANNEL_SECRET)
        print('request META = ' + request.META['HTTP_X_LINE_SIGNATURE'])
        print('body = ' + request.body.decode('utf-8'))
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = webhook.parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if event.message.text == '吃大便' or event.message.text == '呱吉吃大便':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='恭喜答對，以後一起吃大便~耶!')
                    )
                    print(event.source.user_id)
                    models.UserID.objects.create(user_id=event.source.user_id)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=event.message.text)
                    )
            if isinstance(event, FollowEvent):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='請說出通關密語以接收最新消息')
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def push(request):
    line_bot_api.push_message(
        models.UserID.objects.first(),
        TextSendMessage(text='How are you')
    )
    return HttpResponse
