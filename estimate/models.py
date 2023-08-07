from django.db import models
from user.models import CustomUser as User

# Create your models here.

class Estimate(models.Model):
    estimate_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='estimate/%Y/%m/%d', blank=True, null=True)
    content = models.TextField(blank=True)
    dead_line = models.DateTimeField(blank=True)
    # 0 (진행전) 1 (계약진행중) 3 (계약 진행완료)
    status = models.IntegerField(default=0)

class Bookmark(models.Model):
    bookmark_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    estimate_id = models.ForeignKey(Estimate, on_delete=models.CASCADE)

class Tag(models.Model):
    tag_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    estimate_id = models.ForeignKey(Estimate, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)