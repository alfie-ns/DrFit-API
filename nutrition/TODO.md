1. - [x] Need somewhere to store food items eaten (user_id, date, meal_type, food_description, calories)

2. API "add_food_entry" to add food eaten diary/store: API will accept a JSON message:

- [x]
{ "user_id": 1,
  "date": 20230724,
  "meal_type": "dinner",
  "food_description": "chips",
  "calories": 230
}

- [x] could possibly returns calorie summary for the date specified in add entry: eg.

{ "date": 20230724,
  "calories_eaten": 1234,
  "calories_remaining": 1000
}

3. - [x]  Another API "get_calorie_summary" Pass in date:

{ "date": 20230724 }

returns JSON message:

{ "date": 20230724,
  "calories_eaten": 1234,
  "calories_remaining": 1000
}

This API will read all the entries for the chosen data, add together all the calories and
then return this along with the total number of calories they are allowed minus calories eaten.

4. - [x]  API "get_foods_eaten" Pass in date:

{ "date": 20230724 }

returns JSON message:

{ "date": 20230724,
  "foods_eaten": [ {"meal_type": "dinner", "food_description": "chips", "calories": 230},
                   {"meal_type": "dinner", "food_description": "beans", "calories": 200} ]
}
