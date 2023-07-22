from .nutrition_plan import get_age, get_weight, get_height, get_gender
from response.calculations import calculate_calorific_needs
import requests, json, os
from dotenv import load_dotenv
from accounts.models import UserProfile

load_dotenv()

edamam_app_id = "45be5c78"
edamam_app_key = os.getenv("EDAMAM_API_KEY")
url = "https://api.edamam.com/api/food-database/v2/parser"


def get_fooditem(request):  

    data = json.loads(request.body)
    food_item = data.get('food_item')

    user_profile = UserProfile.objects.get(user=request.user)
    daily_calorific_needs = calculate_calorific_needs(user_profile.age, user_profile.height, user_profile.weight, user_profile.goal, user_profile.determination_level, user_profile.activity_level, user_profile.bmr_type, user_profile.gender)
    print(f"USERS CALORIFIC NEEDS = {daily_calorific_needs}")

    if not food_item:
        return {'error': "No food item provided"}

    # Send GET request
    response = requests.get(
        url, 
        params={
            'ingr': food_item,
            'app_id': edamam_app_id, 
            'app_key': edamam_app_key
        }
    )

    # Parse response
    data = response.json()

    # Check for usage limit error
    if data.get('status') == 'error' and data.get('message') == 'Usage limits are exceeded':
        return {'error': 'We are currently experiencing heavy traffic. Please try again later.'}

    # Check if food item was found
    if 'parsed' in data and data['parsed']:
        food = data['parsed'][0]['food']
        food_name = food['label']
        food_calories = food['nutrients']['ENERC_KCAL']
        return {'name': food_name, 'calories': food_calories}
    elif 'hints' in data and data['hints']:
        results = []
        for hint in data['hints']:
            food = hint['food']
            food_name = food['label']
            food_calories = food['nutrients']['ENERC_KCAL']
            results.append({'name': food_name, 'calories': food_calories})
        return results
    else:
        return {'error': f"No information found for {food_item}"}