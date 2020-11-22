from .models import Comment, Reply
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateSerializer, \
    ReplyCreateSerializer, ReplyUpdateSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import bcrypt


class CommentList(APIView):
    """
    댓글 리스트 호출 및 새로운 댓글 생성
    """
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        total_rows = Comment.objects.count()
        per_page = 5
        total_page = int(total_rows / per_page) if total_rows % per_page == 0 else int(total_rows / per_page) + 1

        page = request.GET.get('page')

        try:
            page = int(page)
            if page > total_page:
                page = total_page
        except ValueError:
            page = 1
        except TypeError:
            page = 1

        start_index = (page-1) * per_page
        end_index = start_index + per_page

        comments = Comment.objects.all()[start_index:end_index]

        serializer = CommentListSerializer(comments, many=True)
        return Response({"comments": serializer.data, "total_page": total_page, "current_page": page})

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            encoded_password = serializer.validated_data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            serializer.validated_data['password'] = decoded_hashed_password
            serializer.save()
            comment = Comment.objects.get(pk=serializer.data['id'])
            serializer = CommentListSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """
    댓글 객체 수정 / 삭제
    댓글 비밀번호 확인
    """
    # noinspection PyMethodMayBeStatic
    def get_object(self, pk, nickname, password):
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.nickname == nickname and \
                    bcrypt.checkpw(password.encode('utf-8'), comment.password.encode('utf-8')):
                return comment
            else:
                raise Http404
        except Comment.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        try:
            self.get_object(pk, request.data['nickname'], request.data['password'])
            return Response(status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            comment = self.get_object(pk, request.data['nickname'], request.data['password'])
            serializer = CommentUpdateSerializer(comment, data={
                'nickname': comment.nickname,
                'password': comment.password,
                'content': request.data['content']
            })
            if serializer.is_valid():
                serializer.save()
                comment = Comment.objects.get(pk=serializer.data['id'])
                serializer = CommentListSerializer(comment)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            comment = self.get_object(pk, request.data['nickname'], request.data['password'])
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)


class ReplyCreate(APIView):
    """
    새로운 답글 생성
    """
    # noinspection PyMethodMayBeStatic
    def post(self, request, pk):
        serializer = ReplyCreateSerializer(data=request.data)
        if serializer.is_valid():
            encoded_password = serializer.validated_data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            serializer.validated_data['password'] = decoded_hashed_password
            serializer.save(comment_id=pk)
            comment = Comment.objects.get(pk=pk)
            serializer = CommentListSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDetail(APIView):
    """
    답글 객체 수정 / 삭제
    답글 비밀번호 확인
    """
    # noinspection PyMethodMayBeStatic
    def get_object(self, reply_id, nickname, password):
        try:
            reply = Reply.objects.get(pk=reply_id)
            if reply.nickname == nickname and \
                    bcrypt.checkpw(password.encode('utf-8'), reply.password.encode('utf-8')):
                return reply
            else:
                raise Http404
        except Reply.DoesNotExist:
            raise Http404

    def post(self, request, pk, reply_id):
        try:
            self.get_object(reply_id, request.data['nickname'], request.data['password'])
            return Response(status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, reply_id):
        try:
            reply = self.get_object(reply_id, request.data['nickname'], request.data['password'])
            serializer = ReplyUpdateSerializer(reply, data={
                'nickname': reply.nickname,
                'password': reply.password,
                'content': request.data['content']
            })
            if serializer.is_valid():
                serializer.save()
                comment = Comment.objects.get(pk=pk)
                serializer = CommentListSerializer(comment)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, reply_id):
        try:
            reply = self.get_object(reply_id, request.data['nickname'], request.data['password'])
            reply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)
