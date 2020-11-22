from django.urls import path
from .views import CommentList, CommentDetail, ReplyCreate, ReplyDetail

urlpatterns = [
    path('', CommentList.as_view()),
    path('<int:pk>/', CommentDetail.as_view()),
    path('<int:pk>/reply/', ReplyCreate.as_view()),
    path('<int:pk>/reply/<int:reply_id>/', ReplyDetail.as_view())
]
