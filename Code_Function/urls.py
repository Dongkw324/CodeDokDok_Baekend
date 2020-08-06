from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='code'),
    path('list',views.code_list),
    path('create',views.code_get),
    path('delete',views.code_remove),
    path('userList',views.user_list),
]