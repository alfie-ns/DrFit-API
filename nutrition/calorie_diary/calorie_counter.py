from response.calculations import calculate_calorific_needs, calculate_macronutrient_split
from django.utils.dateparse import parse_date
from django.db.models import Sum
import requests, json, os
from dotenv import load_dotenv
from accounts.models import UserProfile
from ..models import FoodDiaryEntry # Go backwards twice
from datetime import datetime

# Load the environment variables
load_dotenv()

def get_food_search(request):
    edamam_app_id = "45be5c78"
    edamam_app_key = os.getenv("EDAMAM_API_KEY")
    url = "https://api.edamam.com/api/food-database/v2/parser"

    # Get food item requested from app
    data = json.loads(request.body)
    food_item = data.get('food_item')

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
    
def get_food_item(request, food_item):  

    # Get variables needed for API request
    edamam_app_id = "45be5c78"
    edamam_app_key = os.getenv("EDAMAM_API_KEY")
    url = "https://api.edamam.com/api/food-database/v2/parser"

    # Get food item requested from app
    data = json.loads(request.body)
    food_item = food_item
    

    # Get user's calorific needs
    user_profile = UserProfile.objects.get(user=request.user)
    daily_calorific_needs = calculate_calorific_needs(
        user_profile.age, user_profile.height, user_profile.weight,
        user_profile.goal, user_profile.determination_level, user_profile.activity_level,
        user_profile.bmr_type, user_profile.gender)
    
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
    
def get_calorie_summary(request, date_str):
    ''''This function takes in a date_time and 
        returns a calorie summary for that day'''
    
    if request.method == "POST":
        date = parse_date(date_str)

        if date is None:
            return {'error': 'Invalid date.'}
        
        # Calculate the user's calorific needs
        user_profile = UserProfile.objects.get(user=request.user)
        daily_calorific_needs = calculate_calorific_needs(
            user_profile.age, user_profile.height, user_profile.weight, user_profile.goal, 
            user_profile.determination_level, user_profile.activity_level, user_profile.bmr_type, 
            user_profile.gender)
        
        # Filter food diary entries by date and calculate the total calories consumed
        calories_eaten = FoodDiaryEntry.objects.filter(
            user=request.user,
            date_time__date=date).aggregate(Sum('calories'))['calories__sum'] or 0
        
        # Calculate the remaining calories
        remaining_calories = int(daily_calorific_needs) - calories_eaten

        # Prepare and return the response
        response = {
            'date': date_str,
            'calories_eaten': calories_eaten,
            'calories_remaining': remaining_calories
        }
        return response
    else:
        return {'error': 'Invalid request method.'}

def create_food_diary_entry(request):
    '''This function takes in a food item, meal type and date_time
       and creates a food diary entry for the user'''

    if request.method == 'POST':
        #If POST request, get food_item_query and meal_type from app
        data = json.loads(request.body)
        food_item_query = data.get('food_item')
        meal_type = data.get('meal_type')
        date_time = datetime.now()

        # Use get_food_item to retrieve the food's name and calorie count from the Edamam API
        response = get_food_item(request, food_item_query)

        # Check if response is a list (meaning multiple food items found)
        if isinstance(response, list):
            # TODO: sending the list back to the user for selection
            # For now is selecting first item in list
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
        print(f"Food diary entry created successfully for {food_name} at {date_time}")

        date_str = datetime.now().strftime('%Y-%m-%d')  # Convert datetime to a string in the 'YYYYMMDD' format
        calorie_summary = get_calorie_summary(request, date_str)  # Get the calorie summary for today

        return {
            'message': 'Food diary entry created successfully.',
            'calorie_summary': calorie_summary
            }
    else:
        return {'error': 'Invalid request method.'}

def get_foods_eaten(request):
    '''This function takes in a date and returns
       a list of food items eaten on that day'''
    
    # If GET request, get date from app
    if request.method == 'GET':
        data = json.loads(request.body)
        date_string = data.get('date')

        # If no date provided, return error
        if not date_string:
            return {'error': 'No date provided.'}

        # Convert date_string into a date object
        date = datetime.strptime(date_string, '%Y-%m-%d').date()  # adjust the format string according to your needs

        # If the user is not authenticated throw an error
        if not request.user.is_authenticated:  # Checking if the user is authenticated
            return {'error': 'User not authenticated.'}
        
        # Get the daily entries for the user
        daily_entries = FoodDiaryEntry.objects.filter(user=request.user, date_time__date=date)
        
        # If no entries found for the provided date throw an error
        if not daily_entries.exists():  # No entries for the provided date
            return {'error': 'No food entries found for this date.'}

        foods_eaten = [] # Create empty list to store food items eaten
        for entry in daily_entries:
            foods_eaten.append({
                'meal_type': entry.meal_type,
                'food_description': entry.food_item,
                'calories': entry.calories
            }) # Append foods_eaten object to foods_eaten list
        
        return {
                'date': date_string,
                'foods_eaten': foods_eaten}  # Wrap the result in a dictionary

    else:
        # If request method is not GET throw an error
        return {'error': 'Invalid request method.'}