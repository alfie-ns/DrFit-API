from django.urls import path
from .views import DiaryView

urlpatterns = [
    path('diary/', DiaryView.as_view(), name='diary'),
]