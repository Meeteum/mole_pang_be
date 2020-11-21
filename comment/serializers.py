from rest_framework import serializers
from .models import Comment, Reply
import re


class ReplyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'nickname', 'content', 'create_date', 'update_date')


class ReplyCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if re.search(r'\s', data['password']):
            raise serializers.ValidationError("Password는 공백 입력이 안됩니다.")
        if not 0 < len(data['password']) < 8:
            raise serializers.ValidationError("Password는 7자까지입니다.")
        return data

    class Meta:
        model = Reply
        fields = ('id', 'nickname', 'password', 'content', 'create_date', 'update_date')


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'nickname', 'password', 'content', 'create_date', 'update_date')


class CommentListSerializer(serializers.ModelSerializer):
    reply_set = ReplyListSerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'nickname', 'content', 'create_date', 'update_date', 'reply_set')


class CommentCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if re.search(r'\s', data['password']):
            raise serializers.ValidationError("Password는 공백 입력이 안됩니다.")
        if not 0 < len(data['password']) < 8:
            raise serializers.ValidationError("Password는 7자까지입니다.")
        return data

    class Meta:
        model = Comment
        fields = ('id', 'nickname', 'password', 'content', 'create_date', 'update_date')


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'nickname', 'password', 'content', 'create_date', 'update_date')
