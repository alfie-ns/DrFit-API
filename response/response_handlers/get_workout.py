# Path: django-api\response\response_handlers\get_workout.py

'''This file contains functions that will create 
   and return a workout to the user.'''

import openai, os, json, tiktoken, time, random
from accounts.models import UserProfile
from dotenv import load_dotenv
from ..models import Conversation
import http.client

# OpenAI API configuation
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model="gpt-3.5-turbo-16k"

#GET_EXERCISE
def get_exercises():
    conn = http.client.HTTPSConnection("exerciseapi3.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': os.getenv('RAPID_API_KEY'),
        'X-RapidAPI-Host': "exerciseapi3.p.rapidapi.com"
    }
    conn.request("GET", "/exercise/primary_muscle/abs", headers=headers)
    res = conn.getresponse()
    data = res.read()
    exercises = json.loads(data.decode("utf-8"))
    # extract exercise names from the JSON response
    exercise_names = [exercise['name'] for exercise in exercises['exercises']]
    return exercise_names


#GET_WORKOUT
def get_workout(request):
    print("ENTERED GET_WORKOUT FUNCTION")

    # Get workout length from request body
    data = json.loads(request.body.decode('utf-8'))
    workout_length = data.get('workout_length')
    intensity = data.get('intensity')

    #Get conversation
    conversation, created = Conversation.objects.get_or_create(user=request.user)
    print("CONVERSATION: ", conversation)
    # Get user profile
    user_profile = UserProfile.objects.get(user=request.user)
    goal = user_profile.goal
    weight = user_profile.weight
    height = user_profile.height
    age = user_profile.age
    gender = user_profile.gender

    # Get all exercises from external API
    all_exercises = get_exercises()
    print("ALL EXERCISES: ", all_exercises)
    # Randomly select exercises from the list
    number_of_exercises = int(workout_length) // 10 # TODO: work out how many exercises to select based on workout length
    selected_exercises = random.sample(all_exercises, 5) # select 5 random exercises
    print("SELECTED EXERCISES: ", selected_exercises)

    # Prepare the exercise prompt
    exercise_prompt = "I have selected the following exercises: " + ", ".join(selected_exercises) + ". Please use these in my workout plan"


    # Prepare the prompt for the OpenAI API
    workout_prompt = f"""Given my goal {goal} and {workout_length}-minute duration,
                         please tailor a workout plan for a {height}cm, {weight}kg, {age}-year old {gender}.
                         Consider ({exercise_prompt}) also note the Intensity:({intensity}) which is the level
                         of intensity the user wants to go, this will be a number between 1-5, 1 being low intensity
                         and 5 being high intensity which will impact the time rest between each set. Format as:
                        1. Exercise 1 (sets x reps (time required)(time completed)(rest time))))
                        2. Exercise 2 (sets x reps (time required)(time completed)(rest time))))
                        ...
                      """
    # Get messages for get_workout
    messages=[{'role': 'user', 'content': workout_prompt }]
    print(f"WORKOUT PROMPT: {workout_prompt}")
    enc = tiktoken.get_encoding("cl100k_base")
    print(f"TOKEN COUNT FOR WORKOUT PROMPT: {len(enc.encode(workout_prompt))}")
    conversation.history.append({'role': 'user', 'content': workout_prompt})
    start_time = time.time()

    # Prepare the messages parameter for the OpenAI API
    print('ENTERING GET_WORKOUT RESPONSE')
    res = openai.ChatCompletion.create(
        model=model,
        messages=messages + conversation.history,
    )

    # Get the response from the OpenAI API in correct format
    response = res['choices'][0]['message']['content']
    print(f"RESPONSE: {response}")
    print(f"TIME-TAKEN TO GENERATE WORKOUT: {time.time() - start_time}")

    # Add the response to the conversation history
    conversation.history.append({'role': 'assistant', 'content': response})
    conversation.save()
    return response



    
