from django.urls import path
from .views import RankingList

urlpatterns = [
    path('', RankingList.as_view()),
]
