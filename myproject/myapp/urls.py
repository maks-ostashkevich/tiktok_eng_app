from django.urls import path, include
from . import views

urlpatterns = [
    # path('video_list', views.video_list, name='video_list'),
    path('create_exercises/', views.create_exercises, name='create_exercises'),  # New URL for creating exercises
    path('exercise_feed', views.exercise_feed, name='exercise_feed'),
]

