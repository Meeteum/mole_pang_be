from django.urls import path
from .views import CommentList, CommentDetail, ReplyCreate, ReplyDetail

urlpatterns = [
    path('', CommentList.as_view()),
    path('<int:pk>/', CommentDetail.as_view()),
    path('<int:pk>/reply-create/', ReplyCreate.as_view()),
    path('reply/<int:pk>/', ReplyDetail.as_view())
]
