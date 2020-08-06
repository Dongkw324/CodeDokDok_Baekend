from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.db import connection
from django.db import models
from .models import Users
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt)
def indexs(request):
    users=Users.objects.all()
    users=list(users.values())
    return JsonResponse(users,safe=False)

@method_decorator(csrf_exempt)

def user_register(request):
    if request.method=='GET':
        special_user=request.GET.get('user_id',None)
    if request.method=='POST':
        special_user = request.POST.get('user_id', None)  # client로부터 user_id를 받기
    Already = "already joined"
    NoInput="Not inputed user_id"

    if not special_user:  # 만약 받은 user_id가 없으면 {'success':False}를 json형태로 반환
        response = {'success': False,
                    'reason':NoInput}
    elif Users.objects.filter(user_id=special_user).exists():
        response = {'success': False,
                    'reason':Already}
    else:  # 만약 유저가 id를 생성했다면 해당 id를 Users라는 모델에 저장하고 {'success':True}를 json형태로 반환
        user_name = Users(user_id=special_user)
        user_name.save()
        response = {'success': True}

    return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt)
def user_remove(request): #유저 삭제 함수
    special_user=request.POST.get('user_id',None) #query 값으로 user_id를 받아오기

    if not special_user: #해당 data가 없으면 {'success':False}를 json 형태로 반환
        response={'success':False}
    else:
        try:
            #해당 데이터가 있다면, 해당 데이터를 삭제하고 {'success':True}를 json 형태로 반환
            user_name = Users.objects.get(user_id=special_user)
            user_name.delete()  # 해당 유저의 id를 삭제하는 작업
            response = {'success': True}
        except Users.DoesNotExist:
            response={'success':False}
    return JsonResponse(response,safe=False)

# Create your views here.
