import http.client, os, json, random, openai
from dotenv import load_dotenv

load_dotenv()

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

def get_workout():
    # Set OpenAI API configuration
    openai.api_key = os.getenv('OPENAI_API_KEY')
    model="gpt-3.5-turbo"

    # Get all exercises from external API
    all_exercises = get_exercises()
    print("ALL EXERCISES: ", all_exercises)
    # Randomly select few exercises from the list
    selected_exercises = random.sample(all_exercises, 5) # select 5 random exercises
    print("SELECTED EXERCISES: ", selected_exercises)

    # Prepare the exercise prompt
    exercise_prompt = "I have selected the following exercises: " + ", ".join(selected_exercises) + ". Can you include these in my workout plan?"

    # Prepare the workout prompt for the OpenAI API
    workout_prompt =  f"""Considering my goal is to gain muscle, what is the best workout for me?
                          Please construct a personalised workout plan for me that is 60 minutes long
                          and includes the selected exercises. 
                          I am 170cm tall, 70kg, and a 30 years old male. 
                          Factor this information in when constructing the workout plan and personalise it!"""

    # Get messages for get_workout
    messages = [{'role': 'user', 'content': workout_prompt }, {'role': 'system', 'content': exercise_prompt }]

    # Prepare the messages parameter for the OpenAI API
    res = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    # Get the response from the OpenAI API in correct format
    response = res['choices'][0]['message']['content']
    return response

print(get_workout())
