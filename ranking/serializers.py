from rest_framework import serializers
from .models import Ranking


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ('id', 'nickname', 'score', 'play_date', 'ranking')
