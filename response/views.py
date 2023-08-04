# Path: django-api\response\views.py

'''This file contains the classes that will handle the POST request from the app.'''

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .response_handlers.get_response import get_response
from .response_handlers.get_youtube import get_youtube
from .response_handlers.get_workout import get_workout
from .response_handlers.get_initial_plan import get_initial_plan
from .response_handlers.get_personalised_transcript import get_personalised_transcript




# Classes
class GetResponse(APIView):
    @csrf_exempt
    def post(self, request):
        # Parse JSON data from the request body
        response = get_response(request)
        # Return response to app
        return Response({'response': response}, status=status.HTTP_200_OK)

class GetYoutube(APIView):
    @csrf_exempt
    def post(self, request):
        # Parse JSON data from the request body
        response = get_youtube(request)
        # Return response to app
        return Response({'response': response}, status=status.HTTP_200_OK)

class GetWorkout(APIView):
    @csrf_exempt
    def post(self, request):
        # Parse JSON data from the request body
        response = get_workout(request)
        # Return response to app
        return Response({'response': response}, status=status.HTTP_200_OK)
    
class PersonalResponse(APIView):
    @csrf_exempt
    def post(self, request):
        # Parse JSON data from the request body
        response = get_personalised_transcript(request)
        # Return response to app
        return Response({'response': response}, status=status.HTTP_200_OK)