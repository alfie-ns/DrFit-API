from response.calculations import calculate_calorific_needs, calculate_macronutrient_split
from django.utils.dateparse import parse_date
from django.db.models import Sum
from django.db import transaction
from dotenv import load_dotenv
from accounts.models import UserProfile
from ..models import FoodDiaryEntry # Go backwards twice
from response.models import Conversation
from datetime import datetime
import requests, json, os, openai

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
    ''''This function takes in a date and 
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
            date=date).aggregate(Sum('calories'))['calories__sum'] or 0
        print(f"Calories eaten on {date} = {calories_eaten}")
        
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

def manual_create_food_diary_entry(request):
    '''This function takes in a food item, calories, meal type and date
        and manually creates a food diary entry for the user'''
    
    conversation, created = Conversation.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        food_item_name = data.get('food_item_name')
        print(f"Food item name received: {food_item_name}")
        meal_type = data.get('meal_type')
        print(f"Meal type received: {meal_type}")
        calories = data.get('calories') 
        print(f"Calories received: {calories}")
        if calories is None:
            print("No calories provided, using AI model to get calories")
            size = data.get('size') # In grams
            res = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [
                    {"role": "system", "content": f"""You are going to make an accurate conclusion about the calories of {food_item_name} which is 
                                                      the size of {size} grams, just respond only with the number of calories in your response."""},
                ]
            )
            print(f"Raw Response: {res['choices'][0]['message']['content']}")  # prints raw response from the model
            try:
                calories = int(res['choices'][0]['message']['content'])
            except ValueError:
                return {'error': 'Invalid calorie data from AI model.'}

        date_str = data.get('date')  # get the date from the request
        if date_str:
            date_strr = date_str
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # convert the date string to a date
        else:
            date = datetime.now().date()  # use today's date
            date_strr = date.strftime('%Y-%m-%d')  # Convert date to a string in the 'YYYYMMDD' format
        print(f"Date received: {date}")

        FoodDiaryEntry.objects.create(
            user=request.user,
            food_item = food_item_name,
            meal_type=meal_type,
            calories=calories,
            date=date  # use the date
        )
        print(f"Food diary entry created successfully for {food_item_name} at {date} with {calories} calories")
        conversation.history.append({"role": "system", "content": f"Food diary entry created successfully for {food_item_name} at {date} with {calories} calories"})

        calorie_summary = get_calorie_summary(request, date_strr)  # Get the calorie summary for the provided date

        conversation.save()

        return {
            'message': 'Food diary entry created successfully.',
            'calorie_summary': calorie_summary
            }
        
    else:
        return {'error': 'Invalid request method.'}

def create_food_diary_entry(request):
    '''This function takes in a food item, meal type and date
       and creates a food diary entry for the user'''
    
    conversation, created = Conversation.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        #If POST request, get food_item_query and meal_type from app
        data = json.loads(request.body)
        food_item_query = data.get('food_item')
        meal_type = data.get('meal_type')
        date_str = data.get('date')  # get the date from the request
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # convert the date string to a date
        else:
            date = datetime.now().date()  # use today's date
        
        print(f"Food item query received: {food_item_query}")
        print(f"Meal type received: {meal_type}")
        print(f"Date received: {date}")


        # Use get_food_item to retrieve the food's name and calorie count from the Edamam API
        response = get_food_item(request, food_item_query)

        # Check if response is a list (meaning multiple food items found)
        if isinstance(response, list):
            food_name = response[0]['name']
            food_calories = response[0]['calories']
        elif 'error' in response:
            # If there's an error, return the error
            return response
        else:
            # If it's a dictionary (but not an error), proceed as before
            food_name = response['name']
            food_calories = response['calories']
        
            print(f"Food item data received from API: Name - {food_name}, Calories - {food_calories}")

        if food_name is None or food_calories is None:
            return {'error': f"No information found for {food_item_query}"}

        # Create the new FoodDiaryEntry
        FoodDiaryEntry.objects.create(
            user=request.user,
            food_item=food_name,
            meal_type=meal_type,
            calories=food_calories,
            date=date # use the date
        )
        print(f"Food diary entry created successfully for {food_name} at {date} with {food_calories} calories")

        transaction.commit()

        date_str = date.strftime('%Y-%m-%d')  # Convert date to a string in the 'YYYYMMDD' format
        calorie_summary = get_calorie_summary(request, date_str)  # Get the calorie summary for today

        print(f"Calorie summary received: {calorie_summary}")

        conversation.history.append({"role": "system", "content": f"Food diary entry created successfully for {food_item_query} at {date} with {food_calories} calories"})
        conversation.save()

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
        daily_entries = FoodDiaryEntry.objects.filter(user=request.user, date=date)
        
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
                'date': date,
                'foods_eaten': foods_eaten}  # Wrap the result in a dictionary
    
   

    else:
        # If request method is not GET throw an error
        return {'error': 'Invalid request method.'}
    
