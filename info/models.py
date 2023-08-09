from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#공지사항
class Notice(models.Model):
    notice_id = models.IntegerField(primary_key = True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    createtime =  models.DateTimeField()


#배너
class Banner(models.Model):
    id = models.AutoField(primary_key = True)
    image = models.ImageField(upload_to ='banners/') #이미지 저장 경로
    target_url = models.URLField(blank=True, null=True) # 타겟 URL
    display_order = models.IntegerField(default=0) # 표시 순서

    def __str__(self):
        return self.image.url



