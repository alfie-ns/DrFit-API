# Path: django-api\response\response_handlers\get_response.py

import tiktoken, json, openai, os, time
from accounts.models import UserProfile
from django.forms.models import model_to_dict
from ..models import Conversation
from response.utils import *
from dotenv import load_dotenv
from response.calculations import calculate_bmr, calculate_calorific_needs, calculate_bmi, calculate_ideal_body_weight, healthy_weight_calculator, calculate_tdee, calculate_macronutrient_split, calculate_body_fat_percentage, calculate_calories_burnt

# OpenAI API configuation
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model="gpt-4"

# GET_RESPONSE
def get_response(request):
    print("ENTERED GET_RESPONSE FUNCTION")
    print(f"REQUEST: {request.body}")

    # Function call initialization
    function_dict = {
        'calculate_bmr': calculate_bmr,
        'calculate_calorific_needs': calculate_calorific_needs, 
        'calculate_bmi': calculate_bmi,
        'calculate_ideal_body_weight': calculate_ideal_body_weight,
        'healthy_weight_calculator': healthy_weight_calculator,
        'calculate_tdee': calculate_tdee,
        'calculate_macronutrient_split': calculate_macronutrient_split,
        # 'calculate_body_fat_percentage': calculate_body_fat_percentage,
        'calculate_calories_burnt': calculate_calories_burnt
        }
    # List of function descriptions
    functions = [
        calculate_bmr_description,
        calculate_calorific_needs_description,
        calculate_bmi_description,
        calculate_ideal_body_weight_description,
        healthy_weight_calculator_description,
        calculate_tdee_description,
        calculate_macronutrient_split_description,
        # calculate_body_fat_percentage_description,
        calculate_calories_burnt_description
    ]

    # Initialize conversation

    # Get prompt from app
    data = json.loads(request.body)
    user_prompt = data.get('user_prompt')

    # Get user profile
    user_profile = UserProfile.objects.get(user=request.user)
    print(f"USER PROFILE: {user_profile}") # ONLY PRINTS NAME?
    # Convert the UserProfile instance to a dictionary
    user_profile_dict = model_to_dict(user_profile)
    # Prepare the user profile string to be included in the system message
    user_profile_str = ", ".join(f"{key}: {value}" for key, value in user_profile_dict.items())
    print(f"USER PROFILE STRING: {user_profile_str}")

    # Try to get the existing conversation from the database
    conversation, created = Conversation.objects.get_or_create(user=request.user)

    
    print(f"USER PROMPT: {user_prompt}")
    enc = tiktoken.get_encoding("cl100k_base")
    print(f"TOKEN COUNT FOR USER PROMPT: {len(enc.encode(user_prompt))}")
    conversation.history.append({'role': 'user', 'content': user_prompt})
    print(f"CONVERSATION HISTORY: {conversation.history}")
    print(f"GENERAL PROMPT: {general_prompt}")

    start_time = time.time()
    for i in range(5):
        # Get response from OpenAI
        print(f"ENTERING RES_1 call number: {i}")
        err = False
        try:
            res1 = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {'role': 'user', 'content': f"My Details: ({str(user_profile_str)})"},
                    {'role' : 'user',  'content':  f"General Instruction: ({general_prompt})"}  
                ] + conversation.history,
                functions=functions
            )
        except Exception as e:
            print(f"ERROR: {e}")
            err = True
            continue
        print("HERE")
        if not err:
            response_message = res1['choices'][0]['message']
            print(f"RESPONSE MESSAGE RES_1: {response_message}")
            break


    print("OUT OF LOOP")

    # FUNCTION CALL HANDLING
    if 'function_call' in response_message:
        print('FUNCTION CALL DETECTED') 

        function_name = response_message['function_call']['name'] # Get the name of the function to call
        function_to_call = function_dict[function_name] # Get the function to call
        print("=======================", response_message['function_call']['arguments'])
        function_arguments = json.loads(response_message['function_call']['arguments']) # Get the arguments for the function to call

        print(f"Function name: {function_name}\nFunction to call: {function_to_call}\nFunction arguments: {function_arguments}\n")

        function_response = function_to_call(**function_arguments) #Unpack the arguments and call the function
        print("ENTERING RES_2")
        res_2 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                    {"role": "system", "content": general_prompt},
                    {"role": "system", "content": f"User's Details: ({str(user_profile_str)})"},
                    {"role": "function", "name": function_name, "content": function_response},
                    {"role": "user", "content": f"The result of the calculation is {function_response}. How should I interpret this?"}
                    ] + conversation.history,
        )
        response = res_2['choices'][0]['message']['content']
    else:
        print('NO FUNCTION CALL DETECTED')
        response = response_message['content']
    print(f"FINAL RESPONSE: {response}")
    if response == None:
        response = "Error: No response was generated. Please try again."
    print(f"TIME TAKEN TO GENERATE RESPONSE: {time.time() - start_time} seconds")
    # Add the response to the conversation history
    conversation.history.append({'role': 'assistant', 'content': response})
    # Save conversation to database
    conversation.save()
    return response

