from response.calculations import calculate_calorific_needs, calculate_macronutrient_split
from accounts.models import UserProfile

def get_age(request):
    user_profile = UserProfile.objects.get(user=request.user)
    age = user_profile.age
    return age

def get_weight(request):
    user_profile = UserProfile.objects.get(user=request.user)
    weight = user_profile.weight
    return weight

def get_height(request):
    user_profile = UserProfile.objects.get(user=request.user)
    height = user_profile.height
    return height

def get_gender(request):    
    user_profile = UserProfile.objects.get(user=request.user)
    gender = user_profile.gender
    return gender

def calorific_needs(request):
    user_profile = UserProfile.objects.get(user=request.user)
    daily_calorific_needs = calculate_calorific_needs(user_profile)
    return daily_calorific_needs

def macros(request):
    user_profile = UserProfile.objects.get(user=request.user)
    macros = calculate_macronutrient_split(user_profile)
    return macros


