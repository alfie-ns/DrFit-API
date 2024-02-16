from django.db import models
from django.contrib.auth.models import User

class FoodDiaryEntry(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=255)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    calories = models.FloatField()
    date = models.DateField(auto_now_add=True)
