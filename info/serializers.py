from rest_framework import serializers
from .models import Notice, Banner

#공지사항
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['notice_id', 'user_id', 'title', 'content', 'createtime']

#배너
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image', 'target_url', 'display_order']
