from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Problem
from .serializers import ProblemSerializer
import os
from django.conf import settings
import pandas as pd


class InitProblemData(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
            api_key = request.headers['x-api-key']
            if api_key != os.environ.get('API_KEY'):
                raise KeyError
        except KeyError:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        Problem.objects.all().delete()

        problem_data = pd.read_excel(os.path.join(settings.BASE_DIR, 'problem', 'mole_pang_word.xlsx'))

        for index in problem_data.index:
            problem_id = index + 1
            length = problem_data.at[index, '길이']
            consonant = problem_data.at[index, '초성']
            word = problem_data.at[index, '형태']
            meaning = problem_data.at[index, '뜻']

            serializer = ProblemSerializer(
                data={
                    'id': problem_id,
                    'length': length,
                    'consonant': consonant,
                    'word': word,
                    'meaning': meaning
                }
            )

            if serializer.is_valid():
                serializer.save()

        return Response('Success', status=status.HTTP_201_CREATED)
