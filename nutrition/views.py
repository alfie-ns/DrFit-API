from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .calorie_diary.calorie_counter import get_food_item, create_food_diary_entry, get_calorie_summary, get_foods_eaten, get_food_search, manual_create_food_diary_entry
import json

class GetFoodItem(APIView):
    def post(self, request):
        response_data = get_food_item(request)
        if 'error' in response_data:
            return Response({'error': response_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': response_data}, status=status.HTTP_200_OK)

class CreateFoodDiaryEntry(APIView):
    def post(self, request):
        response_data = create_food_diary_entry(request)
        if 'error' in response_data:
            return Response({'error': response_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': response_data}, status=status.HTTP_200_OK)
        
class GetCalorieSummary(APIView):
    def post(self, request):
        data = json.loads(request.body)
        date_str = data.get('date_str')
        response_data = get_calorie_summary(request, date_str)
        if 'error' in response_data:
            return Response({'error': response_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': response_data}, status=status.HTTP_200_OK)
        
class GetFoodsEaten(APIView):
    def get(self, request):
        response_data = get_foods_eaten(request)
        if 'error' in response_data:
            return Response({'error': response_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': response_data}, status=status.HTTP_200_OK)
        
class GetFoodSearch(APIView):
    def post(self, request):
        response_data = get_food_search(request)
        if 'error' in response_data:
            return Response({'error': response_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': response_data}, status=status.HTTP_200_OK)
        
class ManualCreateFoodDiaryEntry(APIView):
    def post(self, request):
        response_data = manual_create_food_diary_entry(request)
        if 'error' in response_data:
            return Response({'error': response_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': response_data}, status=status.HTTP_200_OK)

