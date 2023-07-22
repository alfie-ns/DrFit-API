# Path: drFit\response\response_handlers\get_workout.py

'''This file contains the function that will create 
   and return a workout to the user.'''

import openai, os, json, tiktoken, requests, time, random, datetime, re
from accounts.models import UserProfile
from dotenv import load_dotenv
from ..models import Conversation

# OpenAI API configuation
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model="gpt-3.5-turbo"

#GET_WORKOUT
def get_workout(request):
   print("ENTERED GET_WORKOUT FUNCTION")

   # Get workout length from request body
   data = json.loads(request.body.decode('utf-8'))
   workout_length = data.get('workout_length')

   #Get conversation
   conversation, created = Conversation.objects.get_or_create(user=request.user)


   # Get user profile
   user_profile = UserProfile.objects.get(user=request.user)
   goal = user_profile.goal
   weight = user_profile.weight
   height = user_profile.height
   age = user_profile.age
   gender = user_profile.gender

   # Prepare the prompt for the OpenAI API
   workout_prompt =  f"""Considering my goal is to {goal}, what is the best workout for me?
                         Please construct a personalised workout plan for me that is {workout_length} minutes long.
                         I am {height}cm tall, {weight}kg, and a {age} years old {gender}. Factor this infomation 
                         in when constructing the workout plan and personalise it!"""
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
   print(f"TIME-TAKEN TO GENERATE WORKOUT: {time.time() - start_time}")

   # Add the response to the conversation history
   conversation.history.append({'role': 'assistant', 'content': response})
   conversation.save()
   return response



    
