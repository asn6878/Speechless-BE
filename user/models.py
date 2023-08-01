from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_superuser(self, user_name, email, id, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저는 is_staff=True 여야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저는 is_superuser=True 여야 합니다.")

        return self.create_user(user_name, email, id , password, **extra_fields)
    
    def create_user(self, user_name, email, id, password, **extra_fields):
        if not id:
            raise ValueError("id는 필수입니다.")
        if not password:
            raise ValueError("password는 필수입니다.")
        if not user_name:
            raise ValueError("user_name은 필수입니다.")
        if not email:
            raise ValueError("email은 필수입니다.")

        user = self.model(id=id, password=password, **extra_fields)
        user.set_password(password)
        user.save()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 커스텀 유저 매니저를 사용할것임
    objects = CustomUserManager()

    # 커스텀 유저가 가질 필드들
    user_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    user_name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    id = models.CharField(max_length=20, unique=True)
    prof_img = models.ImageField(blank=True)
    prof_intro = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(default=1)
    exp = models.FloatField(default=0)

    # 권한 관련 필드
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["user_name", "email"]

    def __str__(self):
        return "<user_id : %d / user_name : %s>" % (self.user_id, self.user_name)

    
