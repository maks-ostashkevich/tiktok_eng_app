from django.shortcuts import render, redirect
from .models import Video, AntonymSynonymExercise, GrammarExercise, IdiomExercise, VocabularyExercise, FillInTheBlankExercise, GuessTheTranslationOfTheWord
import json
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


def get_random_exercise():
    exercise_classes = [AntonymSynonymExercise, GrammarExercise, IdiomExercise, VocabularyExercise, FillInTheBlankExercise, GuessTheTranslationOfTheWord]
    ExerciseClass = random.choice(exercise_classes)
    exercises = ExerciseClass.objects.all()
    if not exercises:
        return None
    return random.choice(exercises)


def exercise_feed(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        exercise = get_random_exercise()
        if exercise is not None:
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
        video_file='videos/ensure assure.mp4'  # Make sure this file exists in your media folder
    )

    video_hotel = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/hotel.mp4'  # Make sure this file exists in your media folder
    )

    video_vacation = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/vacation.mp4'  # Make sure this file exists in your media folder
    )

    video_package = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/package.mp4'  # Make sure this file exists in your media folder
    )

    video_dime = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/a dime and dozen.mp4'  # Make sure this file exists in your media folder
    )

    video_bucks = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/big bucks.mp4'  # Make sure this file exists in your media folder
    )

    video_arm_leg = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/cost an arm and a leg.mp4'  # Make sure this file exists in your media folder
    )

    video_quote_price = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/quote a price.mp4'  # Make sure this file exists in your media folder
    )

    video_pp_fill = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/past perfect fill.mp4'  # Make sure this file exists in your media folder
    )

    video_keep_meaning = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/keep meaning.mp4'  # Make sure this file exists in your media folder
    )

    video_continue_meaning = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/continue meaning.mp4'  # Make sure this file exists in your media folder
    )

    video_going_to_aga = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/going to aga.mp4'  # Make sure this file exists in your media folder
    )

    video_will_aga = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/will aga.mp4'  # Make sure this file exists in your media folder
    )

    video_will_be_doing_aga = Video.objects.create(
        title='Example Video',
        description='This is an example video.',
        video_file='videos/will be doing aga.mp4'  # Make sure this file exists in your media folder
    )

    # Create IdiomExercise
    IdiomExercise.objects.create(
        exercise_type='idiom',
        video_1=video_dime,
        video_2=video_bucks,
        video_3=video_arm_leg,
        video_4=video_quote_price,
        question='What is the subject of the idioms in the videos',
        options=json.dumps(['Money', "Health", "Justice", "Insurance"]),
        answer='Money'
    )

    GuessTheTranslationOfTheWord.objects.create(
        exercise_type='guess_the_translation',
        video=video_hotel,
        options=json.dumps(['машина', 'шафа', 'готель', 'карандаш']),
        eng_word='hotel',
        answer='готель',
    )

    GuessTheTranslationOfTheWord.objects.create(
        exercise_type='guess_the_translation',
        video=video_vacation,
        options=json.dumps(['відпустка', 'шафа', 'готель', 'карандаш']),
        eng_word='vacation',
        answer='відпустка',
    )

    GuessTheTranslationOfTheWord.objects.create(
        exercise_type='guess_the_translation',
        video=video_package,
        options=json.dumps(['машина', 'пакет', 'готель', 'карандаш']),
        eng_word='package',
        answer='пакет',
    )

    FillInTheBlankExercise.objects.create(
        exercise_type='fill_in_the_blank',
        video=video_pp_fill,
        part_before_blank = 'I had been',
        part_after_blank = 'before Marie called me.',
        options = json.dumps(['done', 'making', 'sleeping', 'written']),
        answer = 'sleeping',
    )

    # Create AntonymSynonymExercise
    AntonymSynonymExercise.objects.create(
        exercise_type='antonym_synonym',
        video_1=video_continue_meaning,
        video_2=video_keep_meaning,
        question='Are the words \"keep\" and \"continue\" antonyms or synonyms?',
        options=json.dumps(['antonyms', 'synonyms']),
        answer='synonyms'
    )

    # Create GrammarExercise
    GrammarExercise.objects.create(
        exercise_type='grammar',
        video_1=video_going_to_aga,
        video_2=video_will_aga,
        video_3=video_will_be_doing_aga,
        question='Which sentence is grammatically correct?',
        options=json.dumps(["Tom will be playing football all day next Sunday.", 'Tom will play football all day next Sunday.', 'Tom will have played football all day next Sunday.']),
        answer="Tom will be playing football all day next Sunday."
    )

    # Create VocabularyExercise
    VocabularyExercise.objects.create(
        exercise_type='vocabulary',
        video=video,
        word_1='ensure',
        question_1='What does this word mean?',
        options_1=json.dumps(['take (something) away or off from the position occupied', 'make certain that (something) shall occur or be the case', 'leave or cause to leave a place or situation']),
        answer='make certain that (something) shall occur or be the case',
    )

    return redirect('exercise_feed')
