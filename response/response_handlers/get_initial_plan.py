# Path: django-api\response\response_handlers\get_response.py

'''This file contains the function that will
   create the initial plan for the user.'''

import openai, tiktoken, os, time
from dotenv import load_dotenv
from response.utils import system_prompts, goal_descriptions
from response.calculations import calculate_bmi, calculate_ideal_body_weight, calculate_calorific_needs, calculate_bmr, calculate_macronutrient_split 
from response.models import Conversation

# OpenAI API configuation
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model="gpt-4"

# Get initial plan function
def get_initial_plan(user_profile):
   print("ENTERED get_initial_plan FUNCTION")

   # Get user goal description
   detailed_goal = goal_descriptions[user_profile.goal]
   
   # Function calls for initial plan
   daily_calorific_needs = calculate_calorific_needs(user_profile.age, user_profile.height, user_profile.weight, user_profile.goal, user_profile.determination_level, user_profile.activity_level, user_profile.bmr_type, user_profile.gender)
   bmr = calculate_bmr(user_profile.gender, user_profile.age, user_profile.height, user_profile.weight, user_profile.bmr_type)
   bmi = calculate_bmi(user_profile.height, user_profile.weight)
   ideal_weight = calculate_ideal_body_weight(user_profile.gender, user_profile.height)
   macronutrient_split = calculate_macronutrient_split(user_profile.gender, user_profile.height, user_profile.weight, user_profile.bmr_type, user_profile.activity_level, user_profile.age, user_profile.goal)

   # User profile details
   user_profile_details = f"""
   User Profile Details:
   User ID: {user_profile.user.id}
   User Name: {user_profile.user.username}
   User Gender: {user_profile.gender}
   User Age: {user_profile.age}
   User Height: {user_profile.height}
   User Weight: {user_profile.weight}
   User Goal: {detailed_goal}
   User Activity Level: {user_profile.activity_level}
   User Determination Level: {user_profile.determination_level}
   FINAL User Daily Calorific Needs: {daily_calorific_needs} 
   User BMR: {bmr}
   User BMI: {bmi}
   User Ideal Body Weight: {ideal_weight}
   User Macronutrient Split: {macronutrient_split}
   """
   #A multi-line string containing the initial instruction for the AI
   initial_system_message = f"""
   Your Persona: Dr. Fit - an expert virtual personal trainer, nutritionist, and doctor with a profound understanding of human physiology, nutrition, and fitness.

   Task: Create a concise, easy-to-follow bullet-pointed personalized plan for user {user_profile.user.id} to achieve their goal: {detailed_goal}. The plan should be based on the user's provided data and titled "Achieving: {user_profile.goal}".
   User information: {user_profile_details}

   Please follow these guidelines:
   - Address the user directly and in the first person.
   - Focus solely on the essential details.
   - Make the plan approximately 3500 words, including expert detail of every factor of the plan.
   - Maintain a clear and easily understandable bullet list format.
      
   The plan should cover:
   1. The user's daily caloric, bmr, bmi, and macronutrient intake based on their goal. Include food recommendations and meal examples based on {daily_calorific_needs} daily calorific needs.
   2. The high-level longterm fitness plan to achieve their goal({detailed_goal}) in the fastest time possible based on their determination_level({user_profile.determination_level}).
   3. A sleep plan including how to get to sleep fast .
   4. A nutrition plan with the macros required for their goal.
   5. A happiness plan(to be the happiest and confident they can be).
   6. Facts on why they should strive to achieve their goal: {detailed_goal}.
   7. A fact from one of a knowledgeable topic given by Andrew Huberman.
   8. An estimated time frame for goal achievement, again based on how determined they are:({user_profile.determination_level}).
   9. A motivational quote.
   10. Yours sincerely, Dr. Fit, please give me a message if you have any questions!

   Format each plan component as: "<u>Component Title</u>: Component Explanation. Highlight important details in <b>bold tags</b>. Include a link to a relevant website with more information for each point: (<a href="URL" class="response_links">Source</a>).

   Remember do not make your own calculations!!!, they are already done for you, just use the data provided in this prompt.
   """
   initial_stepbystep = f"""
   Your Persona: Dr. Fit - an expert virtual personal trainer, nutritionist, and doctor with a profound understanding of human physiology, nutrition, and fitness. 
   Task: Create a concise, easy-to-follow step-by-step personalized plan for user {user_profile.user.id} to achieve their goal: {detailed_goal}. The plan should be based on the user's provided data and titled "Achieving: {user_profile.goal}".
   User information: {user_profile_details}

   Please follow these guidelines:
   - Address the user directly and in the first person, you are not the user.
   - Focus solely on the essential details.
   - Use a step-by-step format, incorporating checkboxes for each step.
   - Use as many tokens as you need to implement a expert-level of detail, except for the facts of course, as only for steps which the user can complete themselves.

   The plan should cover any very high level plan all steps required to achieve the user's goal,
   including:
   1. The user's daily caloric, bmr, bmi, and macronutrient intake based on their goal. You need to include food recommendations and meal examples based on {daily_calorific_needs} daily calorific needs to achieve their goal as fast as possible.
   2. The high-level longterm fitness plan to achieve their goal({detailed_goal}) in the fastest time possible based on their determination_level({user_profile.determination_level}).
   3. A sleep plan including how to get to sleep fast .
   4. A nutrition plan with the macros required for their goal.
   5. A happiness plan(to be the happiest and confident they can be).

   - They should also be given a fact on why they should strive to achieve their goal: {detailed_goal}.
   - A fact from one of a knowledgeable insight revolving around the users goal: {detailed_goal}. Given by Andrew Huberman. 
   formatted in a step-by-step format with checkboxes for each step.
   - An estimated time frame for goal achievement, again based on how determined they are:({user_profile.determination_level}).
   - A motivational quote.
   - Finally, check what you've send and make sure you've included step-by-step checkboxes for achieving each step and therefore the goal

   Remember do not make your own calculations!!!, they are already done for you, just use the data provided in this prompt.

   """
   enc = tiktoken.get_encoding("cl100k_base")
   print(f"TOKEN COUNT FOR initial_system_message: {len(enc.encode(initial_system_message))}") 
   print(f"TOKEN COUNT FOR initial_stepbystep: {len(enc.encode(initial_stepbystep))}")

   # Create conversation
   # Try to get the existing conversation from the database
   conversation, created = Conversation.objects.get_or_create(user=user_profile.user)

   # If the conversation was just created, initialize an empty history
   if created:
      conversation.history = []

   # Timestamp the start of the initial plan generation
   start_time_initial = time.time()

   res = openai.ChatCompletion.create(
      model='gpt-3.5-turbo',
      messages=[{'role': 'user', 'content': initial_stepbystep}]
   )
   response = res['choices'][0]['message']['content']
   print("INITIAL_PLAN RESPONSE: ", response)

   # Print token count for initial plan 
   print(f"TOKEN COUNT FOR INITIAL_PLAN REQUEST: {len(enc.encode(initial_system_message)) + len(enc.encode(response))}")

   # Timestamp the end of the initial plan generation
   print(f"TIME TAKEN TO GENERATE INITIAL_PLAN: {time.time() - start_time_initial} seconds")

   # Add the response to the conversation history
   conversation.history.append({'role': 'assistant', 'content': response})
   conversation.save() # Save the conversation to the database
   

   return response
