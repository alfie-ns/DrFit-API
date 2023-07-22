from .nutrition_plan import get_age, get_weight, get_height, get_gender
from response.calculations import calculate_calorific_needs
import requests, json, os
from dotenv import load_dotenv
from accounts.models import UserProfile
from .models import FoodDiaryEntry
load_dotenv()


def get_fooditem(request):  

    # Get variables needed for API request
    edamam_app_id = "45be5c78"
    edamam_app_key = os.getenv("EDAMAM_API_KEY")
    url = "https://api.edamam.com/api/food-database/v2/parser"

    # Get food item requested from app
    data = json.loads(request.body)
    food_item = data.get('food_item')

    # Get user's calorific needs
    user_profile = UserProfile.objects.get(user=request.user)
    daily_calorific_needs = calculate_calorific_needs(user_profile.age, user_profile.height, user_profile.weight, user_profile.goal, user_profile.determination_level, user_profile.activity_level, user_profile.bmr_type, user_profile.gender)
    print(f"USERS CALORIFIC NEEDS = {daily_calorific_needs}")

    # If food item is not provided, return error
    if not food_item:
        return {'error': "No food item provided"}

    # Send Edamam-API GET request
    response = requests.get(
        url, 
        params={
            'ingr': food_item,
            'app_id': edamam_app_id, 
            'app_key': edamam_app_key
        }
    )

    # Parse response which means converting it to a dictionary
    data = response.json()

    # Check for usage limit error
    if data.get('status') == 'error' and data.get('message') == 'Usage limits are exceeded':
        return {'error': 'We are currently experiencing heavy traffic for getting food items. Please try again later.'}

    # Check if food item was found
    if 'parsed' in data and data['parsed']: # If there is one food item found  
        food = data['parsed'][0]['food'] # Get the food item
        food_name = food['label'] # Get the name of the food item
        food_calories = food['nutrients']['ENERC_KCAL'] # Get calories from food item
        return {'name': food_name, 'calories': food_calories}
    elif 'hints' in data and data['hints']: # If there are multiple food items found
        results = [] # Create empty list to store hint results
        for hint in data['hints']: # Loop through hints provided
            food = hint['food'] # Get the food item
            food_name = food['label'] # Get the name of the food item
            food_calories = food['nutrients']['ENERC_KCAL'] # Get calories from food item
            results.append({'name': food_name, 'calories': food_calories}) # Append food item to results list
        return results
    else:
        return {'error': f"No information found for {food_item}"}
    
def create_food_diary_entry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        food_item_query = data.get('food_item')
        meal_type = data.get('meal_type')

        # Use get_food_details to retrieve the food's name and calorie count from the Edamam API
        food_name, food_calories = get_fooditem(food_item_query)

        if food_name is None or food_calories is None:
            return {'error': f"No information found for {food_item_query}"}

        # Create the new FoodDiaryEntry
        FoodDiaryEntry.objects.create(
            user=request.user,
            food_item=food_name,
            meal_type=meal_type,
            calories=food_calories
        )

        return {'message': 'Food diary entry created successfully.'}
    else:
        return {'error': 'Invalid request method.'}
