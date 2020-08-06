from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from user.models import Users
import datetime

class Election(models.Model):  # 유저가 로그인했을 때, 해당 유저가 입력한 글들을 볼 수 있는 데이터베이스
    user_name = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )  # User DB와의 연동, 해당 유저의 아이디를 가져오기 위해
    
    site_name = models.CharField(max_length=50, null=False)  # 입력한 사이트명 저장
    recommend_code = models.CharField(max_length=25, null=False,primary_key=True)  # 입력한 추천인 코드 저장
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성시 현재 시간 자동저장

    #해당 유저의 id와 해당 유저가 입력한 사이트명, 추천인코드 반환

    def __str__(self):
        return self.site_name + " " + self.recommend_code

    class Meta:
        ordering = ['-created_at']  # 글 수정 시간 기준으로 오름정렬, 글 쓴 시간 기준으로 내림정렬
# Create your models here.
