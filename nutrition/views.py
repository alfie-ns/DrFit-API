from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .calorie_counter import get_fooditem, create_food_diary_entry

class GetFoodItem(APIView):
    def post(self, request):
        response_data = get_fooditem(request)
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

