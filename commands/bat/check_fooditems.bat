cd .. cd ..

python manage.py shell.py

from nutrition.models import FoodDiaryEntry
# Get all FoodDiaryEntry objects
entries = FoodDiaryEntry.objects.all()

# Loop through and print each entry
for entry in entries:
    print(entry.food_item, entry.meal_type, entry.calories, entry.date)
