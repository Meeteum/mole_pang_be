from .models import Comment, Reply
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateSerializer, \
    ReplyCreateSerializer, ReplyUpdateSerializer, ReplyListSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import bcrypt


class CommentList(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
            댓글(Comment) 리스트 호출

            ---
            ### url: /comment/
            ### method: GET
            ### body request: 없음
            ### 댓글 객체
                {
                    "id": Comment ID,
                    "nickname": Comment 닉네임,
                    "content": Comment 내용,
                    "create_date": Comment 생성일,
                    "update_date": Comment 수정일,
                    "reply_set": [
                        {
                            "id": Reply ID,
                            "nickname": Reply 닉네임,
                            "content": Reply 내용,
                            "create_date": Reply 생성일,
                            "update_date": Reply 수정일
                        }
                    ]
                }
            ### 반환값
                {
                    "comments": 페이징된 댓글 리스트,
                    "total_page": 전체 페이지,
                    "current_page": 현재 페이지,
                    "total_count": 전체 댓글 수
                }
        """
        total_rows = Comment.objects.count()
        per_page = 5
        total_page = int(total_rows / per_page) if total_rows % per_page == 0 else int(total_rows / per_page) + 1
        if total_page == 0:
            total_page = 1
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
        return Response(
            {"comments": serializer.data, "total_page": total_page, "current_page": page, "total_count": total_rows}
        )

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """
            댓글(Comment) 생성

            ---
            ### url: /comment/
            ### method: POST
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호,
                    "content": 댓글 내용
                }
            ### 반환값
                {
                    "id": Comment ID,
                    "nickname": Comment 닉네임,
                    "content": Comment 내용,
                    "create_date": Comment 생성일,
                    "update_date": Comment 수정일,
                    "reply_set": []
                }
        """
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
        """
            댓글(Comment) 비밀번호 확인

            ---
            ### url: /comment/{comment_id}/
            ### method: POST
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호
                }
            ### 반환값
                - 비밀 번호 일치 : Status 204

                - 비밀 번호 불일치 : Status 404
        """
        try:
            self.get_object(pk, request.data['nickname'], request.data['password'])
            return Response(status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """
            댓글(Comment) 업데이트

            ---
            ### url: /comment/{comment_id}/
            ### method: PUT
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호,
                    "content": 댓글 내용
                }
            ### 반환값
                - 정상 처리
                    {
                        "id": Comment ID,
                        "nickname": Comment 닉네임,
                        "content": Comment 내용,
                        "create_date": Comment 생성일,
                        "update_date": Comment 수정일,
                        "reply_set": [
                            {
                                "id": Reply ID,
                                "nickname": Reply 닉네임,
                                "content": Reply 내용,
                                "create_date": Reply 생성일,
                                "update_date": Reply 수정일
                            }
                        ]
                    }

                - 규칙에 맞지 않는 데이터: Status 400

                - 존재하지 않는 ID or 비밀번호 불일치: Status 404
        """
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
        """
            댓글(Comment) 삭제

            ---
            ### url: /comment/{comment_id}/
            ### method: DELETE
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호
                }
            ### 반환값
                - 정상 처리: Status 204

                - 존재하지 않는 ID or 비밀번호 불일치: Status 404
        """
        try:
            comment = self.get_object(pk, request.data['nickname'], request.data['password'])
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)


class ReplyCreate(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request, pk):
        """
            답글(Reply) 생성

            ---
            ### url: /comment/{comment_id}/reply/
            ### method: POST
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호,
                    "content": 댓글 내용
                }
            ### 반환값
                {
                    "id": Reply ID,
                    "nickname": Reply 닉네임,
                    "content": Reply 내용,
                    "create_date": Reply 생성일,
                    "update_date": Reply 수정일
                }
        """
        serializer = ReplyCreateSerializer(data=request.data)
        if serializer.is_valid():
            encoded_password = serializer.validated_data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            serializer.validated_data['password'] = decoded_hashed_password
            serializer.save(comment_id=pk)
            reply = Reply.objects.get(pk=serializer.data['id'])
            serializer = ReplyListSerializer(reply)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDetail(APIView):
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
        """
            답글(Reply) 비밀번호 확인

            ---
            ### url: /comment/{comment_id}/reply/{reply_id}/
            ### method: POST
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호
                }
            ### 반환값
                - 비밀 번호 일치 : Status 204

                - 비밀 번호 불일치 : Status 404
        """
        try:
            self.get_object(reply_id, request.data['nickname'], request.data['password'])
            return Response(status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, reply_id):
        """
            답글(Reply) 수정

            ---
            ### url: /comment/{comment_id}/reply/{reply_id}/
            ### method: PUT
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호,
                    "content": 댓글 내용
                }
            ### 반환값
                - 정상 처리
                    {
                        "id": Reply ID,
                        "nickname": Reply 닉네임,
                        "content": Reply 내용,
                        "create_date": Reply 생성일,
                        "update_date": Reply 수정일
                    }

                - 규칙에 맞지 않는 데이터: Status 400

                - 존재하지 않는 ID or 비밀번호 불일치: Status 404
        """
        try:
            reply = self.get_object(reply_id, request.data['nickname'], request.data['password'])
            serializer = ReplyUpdateSerializer(reply, data={
                'nickname': reply.nickname,
                'password': reply.password,
                'content': request.data['content']
            })
            if serializer.is_valid():
                serializer.save()
                reply = Reply.objects.get(pk=serializer.data['id'])
                serializer = ReplyListSerializer(reply)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, reply_id):
        """
            답글(Reply) 삭제

            ---
            ### url: /comment/{comment_id}/reply/{reply_id}/
            ### method: DELETE
            ### body request
                {
                    "nickname": 닉네임,
                    "password": 비밀번호
                }
            ### 반환값
                - 정상 처리: Status 204

                - 존재하지 않는 ID or 비밀번호 불일치: Status 404
        """
        try:
            reply = self.get_object(reply_id, request.data['nickname'], request.data['password'])
            reply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status.HTTP_404_NOT_FOUND)
