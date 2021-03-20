from django.urls import path
from .views import InitProblemData, ProblemList

urlpatterns = [
    path('', ProblemList.as_view()),
    path('init_problem_data/', InitProblemData.as_view()),
]
