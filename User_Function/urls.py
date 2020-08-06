from django.urls import path
from . import views

urlpatterns=[
    path('',views.indexs,name='user'),
    path('create',views.user_register),
    path('delete',views.user_remove),
]