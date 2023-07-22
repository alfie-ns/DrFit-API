from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets
from .serializers import UserSerializer, UserProfileSerializer
from .models import UserProfile, User


# RegisterView

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny, ] # Allow any user (authenticated or not) to hit this endpoint

    def post(self, request):
        print("REQUEST DATA: ", request.data) # Request data is the data sent in the request(e.g. username, password)
        serializer = UserSerializer(data=request.data) # Serialize the request data
        if serializer.is_valid(): # If serializer is valid(if the data is valid)
            serializer.save() # Save the serializer data
            return Response(serializer.data, status=status.HTTP_201_CREATED) # Return the serializer data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Return a 400 bad request error

# LoginView

class LoginView(APIView):
    permission_classes = [permissions.AllowAny, ] # Allow any user (authenticated or not) to hit this endpoint

    def post(self, request):
        username = request.data.get("username") # Get the username from the request data
        password = request.data.get("password") # Get the password from the request data
        user = authenticate(username=username, password=password) # User is authenticated if the username and password match

        if user is None: # If there is no user
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED) # 401 unauthorized error
        
        token, created = Token.objects.get_or_create(user=user) # Get or create a token for the user
        user_id = Token.objects.get(key=token).user_id # Get user id from the login token
        print(user_id) # Print the user id
        return Response({"token": token.key, "user_id": user_id}, status=status.HTTP_200_OK) # Return the token and user id

# UserProfileViewSet

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can hit this endpoint
    queryset = UserProfile.objects.all() # Get all user profiles and store in queryset
    serializer_class = UserProfileSerializer # Serializer_class is user profile serialized 

    def perform_create(self, serializer):
        # Set the user profile's name to the username
        userprofile = serializer.save()
        userprofile.name = userprofile.user.username
        userprofile.save()

