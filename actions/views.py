from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack
import re
import requests
@csrf_exempt
def event_hook(request):
    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    json_dict = json.loads(request.body.decode('utf-8'))
    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    #return the challenge code here
    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    if 'event' in json_dict:
        event_msg = json_dict['event']
    if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'):
            return HttpResponse(status=200)
    if event_msg['type'] == 'message':
        user = event_msg['user']
        channel = event_msg['channel']
        if re.search(u'[\u4e00-\u9fff]', event_msg['text']):
            request = requests.post('https://labs.goo.ne.jp/api/hiragana', data={'app_id':'d6608540e2e74f08654e07990649c025db831a4c6c2fef51d632db31d67c46b5','sentence': event_msg['text'], 'output_type':'hiragana'})
            parsed = json.loads(request.text)
            channel_id = event_msg['channel']
            thread_ts = event_msg['ts']
            user = event_msg['user']
            response_msg = f"{parsed.get('converted')}"
            client.chat_postMessage(channel=channel, text=response_msg, thread_ts=thread_ts)
        return HttpResponse(status=200)
    return HttpResponse(status=200)