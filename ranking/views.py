from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ranking
from .serializers import RankingSerializer


class RankingList(APIView):
    """
    Ranking 리스트 및 생성(본인 Ranking)
    """

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        ranking = Ranking.objects.all()[:10]
        serializer = RankingSerializer(ranking, many=True)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        serializer = RankingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            my_id = serializer.data['id']
            my_rank = serializer.data['ranking']
            ranking_id_list = \
                [ranking.id for ranking in Ranking.objects.all() if my_rank - 5 <= ranking.ranking <= my_rank + 5]
            ranking = Ranking.objects.filter(id__in=ranking_id_list)
            serializer = RankingSerializer(ranking, many=True)
            return Response({"my_id": my_id, "ranking": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
