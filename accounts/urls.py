from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserProfileViewSet  # ensure UserProfileViewSet is imported

router = DefaultRouter()
router.register('profiles', UserProfileViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # If path is register/, call RegisterView
    path('login/', LoginView.as_view(), name='login'), # If path is login/, call LoginView
    path('', include(router.urls)), # If path is empty, include router.urls
]
