from django.db import models


class Ranking(models.Model):
    nickname = models.CharField(max_length=7, null=False, blank=False)
    score = models.PositiveSmallIntegerField()
    play_date = models.DateTimeField(auto_now_add=True)

    @property
    def ranking(self):
        return list(Ranking.objects.all().values_list('id', flat=True)).index(self.id) + 1

    class Meta:
        app_label = "ranking"
        db_table = "ranking"
        verbose_name = "ranking"
        verbose_name_plural = "ranking"
        ordering = ['-score', '-play_date']
