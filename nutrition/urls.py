from django.urls import path, include
from .views import GetFoodItem, CreateFoodDiaryEntry

urlpatterns = [
    path('get_fooditem/', GetFoodItem.as_view(), name='get_fooditem'),
    path('create_food_diary_entry/', CreateFoodDiaryEntry.as_view(), name='create_food_diary_entry'),
]