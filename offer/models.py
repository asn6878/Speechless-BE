from django.db import models

# 왜래키
from user.models import CustomUser as User
from estimate.models import Estimate


class Offer(models.Model):
    offer_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    estimate_id = models.ForeignKey(Estimate, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    content = models.TextField(blank=True)
    # 0 (진행전) 1 (계약진행중) 3 (계약 진행완료)
    status = models.IntegerField(default=0)