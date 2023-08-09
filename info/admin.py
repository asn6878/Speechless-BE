from django.contrib import admin
from .models import Notice, Banner

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('notice_id', 'user_id', 'title', 'createtime')
    search_fields = ['title']
    list_filter = ('createtime',)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'target_url', 'display_order')

admin.site.register(Notice, NoticeAdmin)
admin.site.register(Banner, BannerAdmin)
