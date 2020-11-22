from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ranking
from .serializers import RankingSerializer


class RankingList(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
            Top 10 랭킹

            ---
            ### url: /ranking/
            ### method: GET
            ### body request: 없음
            ### 랭킹 객체
                {
                    "id": Ranking ID,
                    "nickname": Ranking 닉네임,
                    "score": Ranking 점수,
                    "play_date": Ranking 생성일,
                    "ranking": Ranking 랭킹
                }
            ### 반환값: 랭킹 객체 리스트
        """
        ranking = Ranking.objects.all()[:10]
        serializer = RankingSerializer(ranking, many=True)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """
            랭킹 등록 및 나의 랭킹 확인

            ---
            ### url: /ranking/
            ### method: POST
            ### body request
                {
                    "nickname": 닉네임,
                    "score": 점수
                }
            ### 랭킹 객체
                {
                    "id": Ranking ID,
                    "nickname": Ranking 닉네임,
                    "score": Ranking 점수,
                    "play_date": Ranking 생성일,
                    "ranking": Ranking 랭킹
                }
            ### 반환값
                {
                    "my_id": 등록한 사용자의 ID,
                    "ranking": 등록한 사용자 기준 위아래 5개 Ranking 객체
                }
        """
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
