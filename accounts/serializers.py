from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

# User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Password is write only, so it is not sent around externally

    class Meta: # Meta class for the serializer
        model = User # Model is the User model
        fields = ['username', 'email', 'password'] # Fields are the username, email and password

    def create(self, validated_data):
        user = User( # user is a new user with the validated data
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password']) # Set the password for the user as the validated data['password']
        user.save() # Save the user
        return user # Return the user

'''
This is the UserProfileSerializer class. It's responsible for transforming UserProfile instances into different formats for  
simplicity (serialization) and validating incoming data used to create or update UserProfile instances (deserialization).
The serializer includes the following fields:

- `user`: This is a primary key related field, meaning that it only needs the primary key (id) of the associated user to represent the relationship between User and UserProfile. The field is write-only, which means it will be used during deserialization but won't be included in the serialized output.

- `name`: This field is used to represent the username of the associated User model in the serialized UserProfile data. The value is automatically populated from the 'username' field of the 'user' attribute (user.username). It's read-only, meaning it won't be included in the deserialization, but it will be present in the serialized data.

In the Meta class, we specify the model this serializer is tied to (UserProfile), and that all fields of the model ('__all__') should be included in the serialization/deserialization.

The `create` method defines how a UserProfile instance is created when calling `serializer.save()`. This method extracts the 'user' from the validated data, creates a new UserProfile instance with the remaining validated data and associates it with the User instance. It then returns the created UserProfile instance. 

The `pop` method used on `validated_data` ensures that the 'user' key is removed from the dictionary after it's value is retrieved. This is necessary because 'user' is a write-only field, and shouldn't be included in the UserProfile creation.
'''
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
    def create(self, validated_data):
        user = validated_data.pop('user')
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
