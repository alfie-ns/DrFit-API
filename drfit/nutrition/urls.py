from django.urls import path, include
from .views import GetFoodItem, CreateFoodDiaryEntry, GetCalorieSummary, GetFoodsEaten, GetFoodSearch, ManualCreateFoodDiaryEntry

urlpatterns = [
    path('get_food_item/', GetFoodItem.as_view(), name='get_food_item'),
    path('create_food_diary_entry/', CreateFoodDiaryEntry.as_view(), name='create_food_diary_entry'),
    path('get_calorie_summary/', GetCalorieSummary.as_view(), name='get_calorie_summary'),
    path('get_foods_eaten/', GetFoodsEaten.as_view(), name='get_foods_eaten'),
    path('get_food_search/', GetFoodSearch.as_view(), name='get_food_search'),
    path('manual_create_food_diary_entry/', ManualCreateFoodDiaryEntry.as_view(), name='manual_create_food_diary_entry'),
]