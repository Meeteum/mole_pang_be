from django.contrib import admin
from .models import Problem


class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'length', 'consonant', 'word', 'meaning']


admin.site.register(Problem, ProblemAdmin)
