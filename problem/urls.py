from django.urls import path
from .views import InitProblemData

urlpatterns = [
    path('init_problem_data/', InitProblemData.as_view()),
]
