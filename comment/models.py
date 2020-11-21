from django.db import models


class Comment(models.Model):
    nickname = models.CharField(max_length=7, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    content = models.CharField(max_length=120, null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "comment"
        db_table = "comment"
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ['-create_date']


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=7, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    content = models.CharField(max_length=120, null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "comment"
        db_table = "reply"
        verbose_name = "reply"
        verbose_name_plural = "replies"
        ordering = ['-create_date']
