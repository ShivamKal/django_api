from django.http import JsonResponse
import requests, json
from django.views.decorators.csrf import csrf_exempt
# from ...models import Whatsapp


@csrf_exempt
def userCredentials(request) :
    
    json_body = json.loads(request.body)

    print(json_body)

    api_key = 'A3a69861263f80078b0a7f7efa2b5f495'
    sender_id = 'HXAP1709870428IN'
    channel = 'whatsapp'
    URL = f'https://api-pp-sg.kaleyra.io/v1/{sender_id}/messages'

    postHeader = {
        'Content-Type': 'application/json',
        'api-key': api_key,
    }

    postData = {
        'to' : json_body['to'],
        'type' : json_body['type'],
        'channel' : channel,
        'from' : json_body['from'],
        'body' : json_body['body']
    }

    try :
        post_response = requests.post(url=URL, json=postData, headers=postHeader)
    except ValueError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=500, json=True)

    return JsonResponse(post_response.json())








# def user_exists(id) :  
#     try:
#         wapUser = Whatsapp.objects.get(user_id=id)
#     except Whatsapp.DoesNotExist:
#         return 
#     return wapUser


# def getUser(request):

#     id = request.GET.get('user_id')

#     wapUser = user_exists(id)

#     if wapUser == None :
#         return JsonResponse({'message' : 'Seems like you have not subscribed to whatsapp'}, status_code = 404)
#     else :
#         wapData = {
#             ''
#         }


# def createUser(request) :

#     wapData = {
#         'waba_id' : request.POST.get('waba_id'),
#         'from_number' : request.POST.get('from_number'),
#         'business_id' : request.POST.get('business_id'),
#     }

#     templates :