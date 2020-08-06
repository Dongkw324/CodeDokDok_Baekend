from django.db import models

class Users(models.Model):  # 유저 정보 담을 테이블, 유저의 아이디를 저장함
    user_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.user_id  # 유저 아이디 출력
# Create your models here.
