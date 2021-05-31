from django.contrib import admin
from .models import Ranking


def delete_all_ranking(modeladmin, request, queryset):
    Ranking.objects.all().delete()


class RankingAdmin(admin.ModelAdmin):
    actions = [delete_all_ranking]
    list_display = ['id', 'nickname', 'score', 'play_date']


admin.site.register(Ranking, RankingAdmin)
