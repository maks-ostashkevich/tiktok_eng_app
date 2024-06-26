from django.urls import path, include
from . import views

urlpatterns = [
    # path('video_list', views.video_list, name='video_list'),
    path('', views.index, name='index'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('create_exercises/', views.create_exercises, name='create_exercises'),  # New URL for creating exercises
    path('exercise_feed', views.exercise_feed, name='exercise_feed'),
    path('submit_antonym_synonym/<int:exercise_id>/', views.submit_antonym_synonym, name='submit_antonym_synonym'),
    path('submit_grammar/<int:exercise_id>/', views.submit_grammar, name='submit_grammar'),
    path('submit_pronunciation/<int:exercise_id>/', views.submit_pronunciation, name='submit_pronunciation'),
    path('submit_idiom/<int:exercise_id>/', views.submit_idiom, name='submit_idiom'),
    path('submit_vocabulary/<int:exercise_id>/', views.submit_vocabulary, name='submit_vocabulary'),
]

