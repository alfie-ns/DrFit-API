from response.calculations import calculate_calorific_needs, calculate_macronutrient_split
import requests, json, os
from dotenv import load_dotenv
from accounts.models import UserProfile
from .models import FoodDiaryEntry
load_dotenv()


def get_fooditem(request, food_item):  

    # Get variables needed for API request
    edamam_app_id = "45be5c78"
    edamam_app_key = os.getenv("EDAMAM_API_KEY")
    url = "https://api.edamam.com/api/food-database/v2/parser"

    # Get food item requested from app
    data = json.loads(request.body)
    food_item = food_item

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
    if 'parsed' in data and data['parsed']: # If there is a food item found  
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
        #If POST request, get food_item_query and meal_type from app
        data = json.loads(request.body)
        food_item_query = data.get('food_item')
        meal_type = data.get('meal_type')

        # Use get_fooditem to retrieve the food's name and calorie count from the Edamam API
        response = get_fooditem(request, food_item_query)

        # Check if response is a list (meaning multiple food items found)
        if isinstance(response, list):
            # Do something appropriate here, such as selecting the first item, or sending the list back to the user for selection
            # For now, let's select the first item
            food_name = response[0]['name']
            food_calories = response[0]['calories']
        elif 'error' in response:
            # If there's an error, return the error
            return response
        else:
            # If it's a dictionary (but not an error), proceed as before
            food_name = response['name']
            food_calories = response['calories']

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
