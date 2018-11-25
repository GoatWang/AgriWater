from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
# line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
# parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# @csrf_exempt
# def callback(request):
#     if request.method == 'GET':
#         return JsonResponse({"status_code":200, "message":"you are in callback function!"})
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')

#         try:
#             events = parser.parse(body, signature)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()

#         for event in events:
#             if isinstance(event, MessageEvent):
#                 if isinstance(event.message, TextMessage):
#                     _handle_text_message(event,request.get_host())
#                 if isinstance(event.message, LocationMessage):
#                     _handle_location_message(event)
#             if isinstance(event, FollowEvent):
#                 _handle_follow_event(event)
#             if isinstance(event, UnfollowEvent):
#                 _handle_unfollow_event(event)
#             if isinstance(event, PostbackEvent):
#                 _handle_postback_event(event)
                
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()


def index(request):
    return HttpResponse("Hello, world. You're at the index.")