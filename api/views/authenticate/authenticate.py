from django.http import JsonResponse
from django.db import IntegrityError
from ...models import User, Flag
import time, json
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

'''message for frontend desginer :
    - make sure that following fields during registration are not empty :
        - user_name
        - password
        - fullName
        - email
'''

'''if a record is found with given user-name, it will return the user record (not in json format), else it returns none'''
def user_exists(name):

    try :
        user = User.objects.get(user_data__user_name = name)
    except User.DoesNotExist:
        return None
    return user





'''
function for registering user in the database
    - if success : it will send entire record in json format
    - it failed : it will send respond with an mesaage that registration could not be done
    - if user already exists, a message will to respond that user already exists, try to login 
'''
@csrf_exempt
@api_view(["POST"])
def register(request):

    json_body = json.loads(request.body)
    if user_exists(json_body['user_name'])==None:

        uid = str(int(time.time()))
    
        user_data_dict = {
            'user_name' :  json_body['user_name'],
            'user_password' : make_password(json_body['user_password']),
            'user_fullName' : json_body['user_fullName'],
            'user_email' : json_body['user_email'],
            'user_balance' : 10000
        }

        user_flag_dict = {
            'sms' : False,
            'whatsapp' : False,
            'email' : False
        }

        try:
            new_user = User.objects.create(user_id = uid, user_data = user_data_dict)
            new_flag = Flag.objects.create(user_id = new_user, user_flags = user_flag_dict)

        except IntegrityError as e :
            return JsonResponse( {'message' : str(e)}, status = 404)

    else :
        return JsonResponse( {'message' : "The user_name is already taken! Choose a different user_name"}, status = 401)
    
    # below response will be sent only when user dosen't already exist and records were inserted without any error
    return JsonResponse( {'message' : 'Registration successful', 'user_id' : 123}, status = 200)





'''
login function will send json response :
when success : user_id, message, status_code = 200
when fail : 
    - if user is not registered : error_message, status_code = 404
    - if user gave wrong password : error_message, status_code = 401
'''
@csrf_exempt
def login(request):

    json_body = json.loads(request.body)

    name = json_body['user_name']
    password = json_body['user_password']
    
    user = user_exists(name)

    if user==None :
        return JsonResponse( {'message' : "You're not registered"}, status = 404)
    
    else:
        if check_password(password, user.user_data['user_password']):
            return JsonResponse( {'message' : 'Login Successful!', 'user_id' : user.user_id}, status = 200)
        else:
            return JsonResponse( {'message' : 'Incorrect Password!'}, status = 401)





'''
this will be called by frontend after successful login or registration
it sends :
    - all user_details and 
    - user_flags information as json response
'''
@csrf_exempt
def entrySuccessful(request):

    id = request.GET.get('user_id')
    
    try:
        userInfo = User.objects.get(user_id=id)
    except User.DoesNotExist as e :
        return JsonResponse( {'message' : str(e)}, status = 404)

    try:
        userFlags = Flag.objects.get(user_id = id)
    except Flag.DoesNotExist as e :
        return JsonResponse( {'message' : str(e)}, status = 404)
    

    data = {
        'user_data' : {
            'user_id' : userInfo.user_id,
            'user_name' : userInfo.user_data['user_name'],
            'user_email' : userInfo.user_data['user_email'],
            'user_fullName' : userInfo.user_data['user_fullName'],
            'user_balance' : userInfo.user_data['user_balance'],
        },
        'user_flags' : {
            'sms' : userFlags.user_flags['sms'],
            'whatsapp' : userFlags.user_flags.get('whatsapp', False),
            'email' : userFlags.user_flags['email']
        } 
    }

    return JsonResponse(data)