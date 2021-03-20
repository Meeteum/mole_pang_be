from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Problem
from .serializers import ProblemSerializer
import os
from django.conf import settings
import pandas as pd
import random


class ProblemList(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
            문제 리스트

            ---
            ### url: /problem/
            ### method: GET
            ### body request: 없음
            ### 문제 객체
                {
                    "stage":1,
                    "consonant": "ㄱㅁㅎ",
                    "problem": ["바나나", "고릴라", "만약에", "가만히"],
                    "answer": 3,
                    "meaning": "찌그러져 있다"
                }
            ### 반환값: 문제 객체 리스트
        """
        def get_problem(target_df, consonant):
            correct_word_df = target_df[target_df['consonant'] == consonant].sample()
            wrong_word_df = target_df[target_df['consonant'] != consonant].sample(n=3)

            problem_list = correct_word_df[['word', 'consonant']].values.tolist()
            problem_list.extend(wrong_word_df[['word', 'consonant']].values.tolist())

            random.shuffle(problem_list)

            problem = {
                'consonant': consonant,
                'problem': [lst[0] for lst in problem_list],
                'answer': problem_list.index(correct_word_df[['word', 'consonant']].values.tolist()[0]),
                'meaning': correct_word_df['meaning'].values[0]
            }

            return problem

        def get_consonant_list(target_df, length):
            return random.sample(list(set(target_df['consonant'])), length)

        result = list()

        df = pd.DataFrame(list(Problem.objects.all().values()))

        one_df = df[df['length'] == 1]
        for one_consonant in get_consonant_list(one_df, 10):
            result.append(get_problem(one_df, one_consonant))

        two_df = df[df['length'] == 2]
        for two_consonant in get_consonant_list(two_df, 18):
            result.append(get_problem(two_df, two_consonant))

        three_df = df[df['length'] == 3]
        for three_consonant in get_consonant_list(three_df, 17):
            result.append(get_problem(three_df, three_consonant))

        four_df = df[df['length'] == 4]
        for four_consonant in get_consonant_list(four_df, 5):
            result.append(get_problem(four_df, four_consonant))

        random.shuffle(result)

        for index, r in enumerate(result):
            r['stage'] = index + 1

        return Response(result)


class InitProblemData(APIView):
    swagger_schema = None

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
