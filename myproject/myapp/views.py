from django.shortcuts import render, redirect
from .models import Video, AntonymSynonymExercise, GrammarExercise, PronunciationExercise, IdiomExercise, VocabularyExercise
import json
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def video_list(request):
    video = Video.objects.create(
        title='Video 1',
        description='Video 1 Description',
        video_file='videos/videoplayback (1).mp4'  # Путь к вашему видеофайлу в папке media
    )

    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = Video.objects.get(pk=pk)
    return render(request, 'video_detail.html', {'video': video})


def get_random_exercise():
    exercise_classes = [AntonymSynonymExercise, GrammarExercise, PronunciationExercise, IdiomExercise, VocabularyExercise]
    ExerciseClass = random.choice(exercise_classes)
    exercises = ExerciseClass.objects.all()
    if not exercises:
        return None
    return random.choice(exercises)


def exercise_feed(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        exercise = get_random_exercise()
        if exercise is not None:
            """
            videos = [{'url': video.video_file.url, 'title': video.title} for video in exercise.get_videos()]
            exercise_data = {
                'videos': videos,
                'question': exercise.question,
                'options': list(exercise.options)
            }
            """
            exercise_data = exercise.serialize()
            return JsonResponse({'exercise': exercise_data, 'has_next': True})
        else:
            return JsonResponse({'exercise': None, 'has_next': False})
    else:
        return render(request, 'exercise_feed.html')

def create_exercises(request):
    # Use a single video for simplicity
    video = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/videoplayback.mp4'  # Make sure this file exists in your media folder
    )

    video1 = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/videoplayback (1).mp4'  # Make sure this file exists in your media folder
    )

    video2 = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/videoplayback (2).mp4'  # Make sure this file exists in your media folder
    )

    # Create AntonymSynonymExercise
    AntonymSynonymExercise.objects.create(
        exercise_type='antonym_synonym',
        video_1=video2,
        video_2=video1,
        question='Are these words antonyms or synonyms?',
        options=json.dumps(['antonym', 'synonym']),
        answer='synonym'
    )

    # Create GrammarExercise
    GrammarExercise.objects.create(
        exercise_type='grammar',
        video_1=video2,
        video_2=video,
        video_3=video1,
        question='Which sentence is grammatically correct?',
        options=json.dumps(['Option 1', 'Option 2', 'Option 3']),
        correct_option='Option 1'
    )

    # Create PronunciationExercise
    PronunciationExercise.objects.create(
        exercise_type='pronunciation',
        video_1=video1,
        video_2=video2,
        video_3=video,
        word='example'
    )

    # Create IdiomExercise
    IdiomExercise.objects.create(
        exercise_type='idiom',
        video_1=video,
        video_2=video1,
        video_3=video2,
        video_4=video,
        question='What do these idioms mean?',
        options=json.dumps(['Option 1', 'Option 2', 'Option 3', 'Option 4']),
        correct_option='Option 1'
    )

    # Create VocabularyExercise
    VocabularyExercise.objects.create(
        exercise_type='vocabulary',
        video=video,
        word_1='example_word_1',
        word_2='example_word_2',
        question_1='What does this word mean?',
        question_2='What does this word mean?',
        options_1=json.dumps(['Option 1', 'Option 2', 'Option 3']),
        options_2=json.dumps(['Option 1', 'Option 2', 'Option 3']),
        correct_option_1='Option 1',
        correct_option_2='Option 1'
    )

    return redirect('exercise_feed')

def submit_antonym_synonym(request, exercise_id):
    exercise = AntonymSynonymExercise.objects.get(id=exercise_id)
    answer = request.POST.get('answer')
    score = 1.0 if answer == exercise.answer else 0.0
    return redirect('exercise_feed')

def submit_grammar(request, exercise_id):
    exercise = GrammarExercise.objects.get(id=exercise_id)
    answer = request.POST.get('answer')
    score = 1.0 if answer == exercise.correct_option else 0.0
    return redirect('exercise_feed')

def submit_pronunciation(request, exercise_id):
    exercise = PronunciationExercise.objects.get(id=exercise_id)
    # Implement pronunciation check logic
    score = 1.0  # Placeholder score
    return redirect('exercise_feed')

def submit_idiom(request, exercise_id):
    exercise = IdiomExercise.objects.get(id=exercise_id)
    answer = request.POST.get('answer')
    score = 1.0 if answer == exercise.correct_option else 0.0
    return redirect('exercise_feed')

def submit_vocabulary(request, exercise_id):
    exercise = VocabularyExercise.objects.get(id=exercise_id)
    answer_1 = request.POST.get('answer_1')
    answer_2 = request.POST.get('answer_2')
    score_1 = 1.0 if answer_1 == exercise.correct_option_1 else 0.0
    score_2 = 1.0 if answer_2 == exercise.correct_option_2 else 0.0
    return redirect('exercise_feed')


"""
    # Fetch random exercises for the feed
    antonym_synonym_exercises = AntonymSynonymExercise.objects.all().order_by('?')[0]
    grammar_exercises = GrammarExercise.objects.all().order_by('?')[0]
    pronunciation_exercises = PronunciationExercise.objects.all().order_by('?')[0]
    idiom_exercises = IdiomExercise.objects.all().order_by('?')[0]
    vocabulary_exercises = VocabularyExercise.objects.all().order_by('?')[0]

    context = [antonym_synonym_exercises, grammar_exercises, pronunciation_exercises, idiom_exercises, vocabulary_exercises]
    return render(request, 'exercise_feed.html', {'exercises': context})

    page = request.GET.get('page', 1)
    paginator = Paginator(exercises_list, 5)  # Number of exercises per page

    try:
        exercises = paginator.page(page)
    except PageNotAnInteger:
        exercises = paginator.page(1)
    except EmptyPage:
        exercises = paginator.page(paginator.num_pages)

    return render(request, 'exercise_feed.html', {'exercises': exercises})
    """

"""
    context = {
        'antonym_synonym_exercises': antonym_synonym_exercises,
        'grammar_exercises': grammar_exercises,
        'pronunciation_exercises': pronunciation_exercises,
        'idiom_exercises': idiom_exercises,
        'vocabulary_exercises': vocabulary_exercises,
    }
"""