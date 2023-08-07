# DR-FIT(API) - Django REST Framework
#### On setup
**New venv** -> python -m venv venv
**Activate venv** -> .\venv\Scripts\activate
**New Requirements** -> pip freeze > requirements.txt
**Install requirements** -> pip install -r requirements.txt

## Commands
#### Virtual Environment
- python -m venv venv -> create new venv
- .\venv\Scripts\activate -> activate virtual environment
- deactivate -> deactivate virtual environment
#### Django
- python manage.py runserver -> run server
- python manage.py startapp <app_name> -> create new app
- python manage.py createsuperuser -> create superuser
- python manage.py makemigrations -> create migrations
- python manage.py migrate -> migrate migrations
#### Postgres
##### Look in database
- psql -h localhost -U ANurs -d django-db 
- (password on .env)


# Phone notes
- [ ] When fomulating advice, use calculations depending on what it wants to say. e.g. "What else should I eat today?" -> Calculate_calorific_needs - food counted that day
- [x] Bodyfat percentage as optional field
- [ ] Clear conversation api request
- [x] When creating initial plan, think of steps the user can tick off
- [x] Save initial plan somewhere
- [ ] Nutritional calorie counter diary
- [x] Change database password and put in .env file
- [ ] COMPONENT-STREAMING/LOADING SCREEN FOR API GET RESPONSE

## Calorie counter idea


## Diary
- [x] I have recently started making the initial plan and now need the make the get request(find where userprofile is created and then call the function that makes initial plan inside models.py?, then get)
- [x] I'm trying to get the initial plan to put it in the diary app
- [ ] food calorie diary: implement a way to search for food items and then add them to the diary which minus of the daily calorific needs
- [ ] Make sure the personal youtube prompter is working

## Dad
- [ ] Implementing checkboxex
- [ ] Implementing strava api

## Plan

- [x] Create .env file
- [x] Get OpenAI API Working
- [x] Get PostMan Working
- [x] Extra registeration for profile 
- [x] Test user profile with dad quickly(test creating a user and user profile, list_users.bat shows all users in database)
- [x] Get user profile working with gpt
- [x] Create a memory for the gpt to use
- [x] Set up function calls
- [x] ?DONE? Prompt engineer api to always remember it has user profile in order to call functions ?DONE?
- [x] Put chatcompletion for response in seperate file
- [x] Calls function but also attempts to recaculate it itself(RESET DATABASE AND NOW IT WORKS?)
- [x] YouTube implementation
- [x] Engineer function call prompts
- [x] Set up host-email
- [x] Make conversation history seperate for each user
- [x] Add initial plan to conversation history
- [x] Add workout plan in conversation history
- [x] Implement youtube functionality where the user can select how many insights they want to see
- [x] Youtube insight memory?
- [x] Sort out calorific needs calculation(Might need more checks)
- [x] Engineer YouTube prompt
- [x] Making userprofile: name = user: username
- [x] Create initial plan
- [x] Create workout_plan generator
- [x] Implement calorie counter diary(get calorific needs of certain food items)



- [x] BRAIN NUTRIENTS YOUTUBE PROMPT: https://www.youtube.com/watch?v=E7W4OQfJWdw&t=1880s
- [ ] Get gpt read over the entire youtube video, then implement a prompt for the user to ask for specific insights
- [ ] Speed up youtube sumarization
- [ ] Make gpt know everything that's happening in the app
- [ ] OpenAI edamam food-database specification ???
- [ ] Implement milestones
- [ ] Figure out registeration(What connects a user and userprofile?) - DAD
- [ ] Use functions when giving advice and create examples to teach when to use them
- [x] Create Inital-plan with steps 
- [ ] Allow the steps to be ticked off
- [x] Bodyfat percentage as optional field
- [ ] anti-cheating functonality
- [ ] If error with function call try again until it's worked OR give up after 5 attempts and display error
- [ ] Clear GPT conversation for specific user
- [ ] SORT OUT THE MET VALUE FOR RUNNING WITH SPEED = DISTANCE/TIME. CONVERT MILES AND KM TO METRES
- [ ] Make other BMI calculations: https://www.calculator.net/bmi-calculator.html
- [ ] Finish calories burnt calculation function, maybe get gpt to decide on the specific funtion depending on the user's activity?
- [ ] gpt to create nutrition plans in nutitition.py?: https://spoonacular.com/food-api, function call spoonecular api
- [ ] gpt to create workout plans in workout.py?: https://wger.de/en/software/api, https://developers.strava.com/ wger 
- [ ] Strava api (running leagues) 
- [ ] complete registeration checks
- [ ] Opitmize function speed by not connecting to the database inside the functions
- [ ] Work out the optimal way for calculating calories for every goal
- [ ] Implementing youtube transcripts
- [ ] Calculate everything with function calls passed to openai api
- [ ] Implement a way to measure user's health and fitness level? (apple health)
- [ ] test image generation with simple functional pictures
- [ ] Implement best pracitices in prompting: https://platform.openai.com/docs/guides/gpt-best-practices
- [ ] give the functions to the GPT to function call and make a report
- [ ] FINALLY Implement load-balancing

# ADVANCED CALCULATION FUNCTIONS
- [ ] Waist to Height Ratio
- [ ] Waist to Hip Ratio
- [ ] Lean Body Mass
- [ ] Fat Mass
- [ ] VO2 Max
- [ ] One Rep Max (1RM)
- [ ] Pace and Split Times for Running/Cycling/Swimming
- [ ] Protein Requirement
- [ ] Hydration Requirement

## Features to include in the app:

- [ ] Sleep page 
- [x] Personalized workout plans: Based on the user's input, provide customized workout plans that target specific muscle groups, cater to their fitness level, and help achieve their goals.
- [ ] Nutrition advice: Offer personalized meal plans and recipes that take into account the user's calorific needs, dietary preferences, and any specific health conditions or restrictions.
- [ ] Goal setting: Encourage users to set realistic short-term and long-term fitness goals, and provide regular check-ins to track progress and adjust plans accordingly.
- [ ] Exercise demonstrations: Provide video demonstrations or detailed instructions for a wide range of exercises, including proper form and technique to prevent injuries.
- [ ] Progress tracking: Integrate a feature that tracks user's progress (e.g., weight change, exercise performance, completed workouts) and offers insights, motivation, and encouragement.
- [ ] Health tips and resources: Share general health and wellness advice, covering topics like sleep, stress management, and hydration.
- [ ] Community support: Create a platform for users to connect with others, ask questions, share experiences, and offer support.
- [ ] Expert consultations: Offer access to certified personal trainers, nutritionists, or other health professionals for personalized advice and guidance.
- [ ] Challenges and rewards: Create fitness challenges and offer rewards to keep users engaged and motivated to stay on track.
- [ ] Integration with wearables and other apps: Allow users to connect your app to their wearable devices (e.g., fitness trackers, smartwatches) or other health and fitness apps for a more comprehensive experience.

## Design and development considerations:

- [ ] User-friendly interface: Design an intuitive and visually appealing user interface that is easy to navigate, making the user experience seamless and enjoyable.
- [ ] Data privacy and security: Ensure user data is stored securely and in compliance with data protection regulations. Be transparent about how the data is used and provide users with options to manage their data privacy.
- [ ] Regular updates and improvements: Continuously update your app with new features, content, and improvements based on user feedback and industry trends to keep users engaged and maintain relevance.
- [ ] Accessibility: Make your app accessible to a diverse user base, including people with disabilities, by following accessibility guidelines (e.g., text size, color contrast, screen reader compatibility).
- [ ] Multi-device and platform support: Ensure your app is compatible with various devices (e.g., smartphones, tablets) and platforms (e.g., iOS, Android) to reach a wider audience.
- [ ] Onboarding and tutorials: Provide a clear onboarding process and tutorials to help new users understand how to use your app effectively and get the most value from its features.
- [ ] Customer support: Offer responsive and helpful customer support to address user concerns, provide assistance, and gather valuable feedback.
- [ ] Marketing and promotion: Develop a marketing strategy to promote your app, including social media, content marketing, and app store optimization to increase visibility and attract new users.
- [ ] Monetization: Consider different monetization strategies, such as in-app purchases, subscriptions, or ads, to generate revenue while maintaining a positive user experience.
- [ ] Testing and quality assurance: Conduct thorough testing and quality assurance to identify and fix bugs, ensure app stability, and provide a smooth user experience.

## Authentication:

- [ ] Email and password: Create an account using email address and unique password, with secure password storage and retrieval methods for user data security.
- [ ] Social media logins: Integration with Facebook, Google, or Apple for simplified login using existing accounts.
- [ ] Single Sign-On (SSO): Implementation of services like Okta, Auth0, or Azure Active Directory for login with credentials from other services.
- [ ] Two-factor authentication (2FA): Extra security layer requiring identity verification through additional methods (e.g., SMS, authenticator app) after email and password entry.
- [ ] Biometric authentication: Integration with fingerprint, face recognition, or iris scanning options (available on some devices) for secure and convenient login.
- [ ] Passwordless authentication: Implementation of Magic Links or authentication codes sent via SMS for password-free login.
- [ ] OAuth providers: Integration with Microsoft, LinkedIn, or Twitter for login using existing accounts on these platforms.
- [ ] Third-party fitness apps: Login using existing accounts on popular fitness apps like MyFitnessPal, Strava, or Runkeeper.


## OPENAI API Waiting-time tasks
- [ ] User's Progress Report: Show them their progress, such as workouts completed, calories burned, or steps walked. You can use visually appealing graphs and charts for this.

- [ ] Educational Content: Share fitness tips, articles, and videos that are relevant to the user's goals. This could be an article about diet, a video tutorial for a specific exercise, or general advice on maintaining motivation.

- [ ] Interactive Content: Quiz them on fitness knowledge or provide interactive content such as mini-games related to fitness.

- [ ] Community Engagement: If your app has a community aspect, show them updates from other users, or even prompt them to engage with others.

- [ ] Goal Setting: Provide them with an interface to set or adjust their goals, or review their current goals and achievements.

- [ ] Motivational Quotes or Success Stories: Display motivational quotes or success stories from other users to inspire them.

- [ ] Personalized Workout or Diet Plans: Show them their upcoming workouts or meal plans if they have one.

- [ ] Relaxation Techniques: Guide them through a short mindfulness or breathing exercise.

- [ ] Feedback or Reviews: Ask for their feedback on the app or prompt them to review the app.

- [ ] Notifications Review: Show them their past achievements or remind them of their future workouts.


## USER PROMPT IDEAS:

1. What are the best exercises for weight loss and overall fitness?

2. How do I create a balanced diet plan that promotes good health and supports my fitness goals?

3. Can you provide tips for improving sleep quality to aid in recovery and overall well-being?

4. As a beginner, what are the most essential elements I should focus on in building an effective workout routine?

5. How can I manage stress to improve my overall health and mental well-being?

6. Could you recommend specific exercises to help improve posture and alleviate back pain?

7. How can I stay motivated and consistent with my fitness and nutrition program?

8. What are the differences between various types of cardio exercises (e.g., running, swimming, cycling), and which one is best for me?

9. How can I build and maintain muscle mass as I age?

10. What are some warning signs of overtraining, and how can I ensure I'm giving my body adequate rest and recovery?

11. Can you provide guidelines for staying hydrated during exercise, considering factors like workout intensity and duration?

12. How should I adjust my nutrition and workout routines if I have a specific medical condition (e.g., diabetes, high blood pressure)?

13. What are the benefits of incorporating functional training exercises into my workout routine?

14. How can I safely and effectively increase my flexibility and mobility?

15. What strategies can I use to overcome common obstacles to sticking with a fitness and nutrition plan, such as lack of time, limited resources, or lack of support?

16. What are some ways to improve my mental health and well-being?

17. How can I improve my gut health and digestion?

18. What are the benefits of using a sauna, and how often should I use it?

19. How can I improve my cardiovascular endurance?

20. What are the best exercises for building muscle and strength?

## Server management

1. **Backups**: Regularly back up your data to protect against data loss. 

2. **Redundancy**: Implement redundancy in your system. This might involve load-balanced servers, multiple database instances, or both. In case one component fails, the others can take over, and your app remains operational.

3. **Atomic Transactions**: Use atomic transactions in your database operations. This ensures that your operations (like writes and updates) either fully complete or don't happen at all, minimizing the chance of data corruption.

4. **Monitoring and Alerts**: Implement robust monitoring and alert systems to detect and notify about any issues as soon as they arise. 

5. **Testing**: Thoroughly test your app, including load testing and stress testing, to ensure it can handle expected user traffic and interactions.

6. **Gradual Deployment**: Use strategies like blue-green deployments, canary releases, or rolling updates to gradually roll out changes to all users. These strategies allow you to minimize the risk associated with deployment and quickly roll back if issues are detected.

7. **Disaster Recovery Plan**: Have a disaster recovery plan in place, including how to restore from backups, failover to redundant systems, and steps to diagnose and fix issues.

## Security(Not Finished)

## Test Plan(Not Finished)

## High level plan:

Homepage:
a. Sign Up/Login
b. User Profile & Settings
c. Plan Overview

Plan Overview:
a. Meal Plan
b. Workout Plan
c. Sleep Page
d. Saunas & Health Benefits

Meal Plan:
a. Personalized Recipes
b. Nutritional Information
c. Meal Difficulty Filter
d. Save/Delete Plan

Workout Plan:
a. Personalized Workouts
b. Exercise Demonstrations
c. Progress Tracking
d. Save/Delete Plan

Sleep Page:
a. Sleep Recommendations
b. Sleep Tracking

Saunas & Health Benefits:
a. Information on Sauna Benefits
b. Recommendations for Sauna Use

Community:
a. User Forums
b. Expert Consultations
c. Challenges & Rewards
d. Leagues & Points System

Integrations:
a. Wearables & Fitness Apps
b. Authentication Options

Customer Support & Resources:
a. Health Tips & Resources
b. Contact & Support
c. Tutorials & Onboarding

Settings & Privacy:
a. User Profile
b. Data Privacy & Security
c. Accessibility Options
d. Logout
