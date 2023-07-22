from django.urls import path, include
from .views import GetFoodItem

urlpatterns = [
    path('get_fooditem/', GetFoodItem.as_view(), name='get_fooditem'),
]