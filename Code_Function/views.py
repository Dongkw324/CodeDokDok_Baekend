from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .models import Election,Users
from django.db import models
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
import random

@method_decorator(csrf_exempt)
def index(request):
    codes=Election.objects.all()
    codes=list(codes.values())
    return JsonResponse(codes,safe=False)

@method_decorator(csrf_exempt)
def code_list(request): #코드 리스크 검색 함수
    codes = Election.objects.all()
    codes = Election.objects.order_by('created_at').reverse().values()
    #query값으로 search, count를 받아오기
    search=request.GET.get('site_name',None)
    count=10
    if not search: #search값이 없으면 query값으로 page변수명 이용
        paginator = Paginator(codes, count)
        page = request.GET.get('page')
        try:
            code = paginator.page(page)
        except PageNotAnInteger: #입력된 page가 없으면 첫 번째 page 출력 (예외처리)
            code = paginator.page(1)
        except EmptyPage:
            return JsonResponse(None,safe=False)
        return JsonResponse(list(code), safe=False)
    codes = codes.filter(site_name__icontains=search) #site명 검색 구현
    #if not codes: #해당 site명이 없으면 null값 리턴
     #   response = {'success': False,
      #               'reason': None}
       # return JsonResponse(response, safe=False)
    pagination=Paginator(codes,count) #search값이 있을 시에는 query값으로 specific_page변수명 이용
    specific_page=request.GET.get('specific_page')
    try:
        site=pagination.page(specific_page)
    except PageNotAnInteger:
        site=pagination.page(1)
    except EmptyPage:
        return JsonResponse(None,safe=False)
    return JsonResponse(list(site), safe=False)

@method_decorator(csrf_exempt)
def code_get(request): #코드 생성 함수
        # Query값으로 site와 code, 그리고 user_id를 이용(사용자의 정보, 사용자가 입력한 site명, code명을 받아옴)
    my_site = request.POST.get('site_name', None)
    my_code = request.POST.get('recommend_code', None)
    my_user_id = request.POST.get('user_name', None)
    Already="Already Used recommend_code"
    NoInput="No Input data"
    NoUserId="No User Id"
    if not(my_site and my_code):
        response={'success':False,
                  'reason':NoInput}
    elif Election.objects.filter(recommend_code=my_code).exists():
        response={'success':False,
                  'reason':Already}
    else:
        # 해당 유저가 입력한 코드명, 사이트명 저장하고 그것들을 불러옴
        try:
            users = Users.objects.get(user_id=my_user_id)
            user_instance = Election(user_name=users, site_name=my_site, recommend_code=my_code)
            user_instance.save()
            response = {'success': True}  # 만약 코드와 사이트를 생성했다면 {success:true}를 json 형태로 반환
        except Users.DoesNotExist:
            response={'success':False,
                      'reason':NoUserId}
    # JsonResponse(결과 출력)
    return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt)
def code_remove(request): #코드 제거(삭제) 함수
    #query 값으로 recommend_code를 받아와서 my_code에 저장
    my_code=request.POST.get('recommend_code',None)

    if not my_code: #my_code에 해당하는 데이터가 db에 없다면 {'success':False}를 json 형태로 반환
        response={'success':False}
    else: #만약 해당하는 데이터가 있다면 그 데이터를 가지고 와서 삭제한 후 {'success':True}를 json 형태로 반환
        try:
            code_list=Election.objects.get(recommend_code=my_code)
            code_list.delete()
            response={'success':True}
        except Election.DoesNotExist:
            response={'success':False}

    return JsonResponse(response,safe=False)

def user_list(request):
    codes=Election.objects.all()
    user_name=request.GET.get('user_id',None)
    NotUser="No User Name"
    NoResult="No result of searching"

    if not user_name:
        response={'success':False,
                  'reason':NotUser}
        return JsonResponse(response,safe=False)
    else:
        try:
            user_id=Users.objects.get(user_id=user_name)
            user_site=codes.filter(user_name=user_id)
            if not user_site:
                response={'success':False,
                          'reason':NoResult}
                return JsonResponse(response,safe=False)
            user_site=list(user_site.values())
            return JsonResponse(user_site,safe=False)
        except Users.DoesNotExist:
            response={'success':False,
                      'reason':NotUser}
            return JsonResponse(response,safe=False)

# Create your views here.
