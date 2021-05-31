from django.contrib import admin
from .models import Comment, Reply


def delete_all_comment(modeladmin, request, queryset):
    Comment.objects.all().delete()


class CommentAdmin(admin.ModelAdmin):
    actions = [delete_all_comment]
    list_display = ['id', 'nickname', 'content', 'create_date', 'update_date']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'nickname', 'content', 'create_date', 'update_date']
    list_display_links = ['comment']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
