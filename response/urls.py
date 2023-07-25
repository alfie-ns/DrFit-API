from django.urls import path, include
from .views import GetResponse
from .views import GetYoutube
from .views import GetWorkout
from .views import PersonalResponse



urlpatterns = [
    path('get_response/', GetResponse.as_view(), name='get_response'),
    path('get_youtube/', GetYoutube.as_view(), name='get_youtube'),
    path('get_workout/', GetWorkout.as_view(), name='get_workout'), 
    path('get_personalised_transcript/', PersonalResponse.as_view(), name='personalised_transcript')   

]