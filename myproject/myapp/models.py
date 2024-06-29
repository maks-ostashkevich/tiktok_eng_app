from django.db import models
import json

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BaseExercise(models.Model):
    exercise_type = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def serialize(self):
        raise NotImplementedError("Subclasses must implement this method")

class AntonymSynonymExercise(BaseExercise):
    video_1 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='antonym_synonym_video_1')
    video_2 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='antonym_synonym_video_2')
    question = models.CharField(max_length=255)
    options = models.JSONField()  # A JSON field to store multiple choice options
    answer = models.CharField(max_length=50)  # 'antonym' or 'synonym'

    def get_videos(self):
        return [getattr(self, f'video_{i}') for i in range(1, 3)]

    def serialize(self):
        return {
            'type': 'antonym_synonym',
            'videos': [{'url': video.video_file.url, 'title': video.title} for video in self.get_videos()],
            'question': self.question,
            'options': json.loads(self.options),
            'answer': self.answer,
        }

class GrammarExercise(BaseExercise):
    video_1 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='grammar_video_1')
    video_2 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='grammar_video_2')
    video_3 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='grammar_video_3')
    question = models.CharField(max_length=255)
    options = models.JSONField()  # A JSON field to store multiple choice options
    answer = models.CharField(max_length=50)

    def get_videos(self):
        return [getattr(self, f'video_{i}') for i in range(1, 4)]

    def serialize(self):
        return {
            'type': 'grammar',
            'videos': [{'url': video.video_file.url, 'title': video.title} for video in self.get_videos()],
            'question': self.question,
            'options': json.loads(self.options),
            'answer': self.answer,
        }

class IdiomExercise(BaseExercise):
    video_1 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='idiom_video_1')
    video_2 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='idiom_video_2')
    video_3 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='idiom_video_3')
    video_4 = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='idiom_video_4')
    question = models.CharField(max_length=255)
    options = models.JSONField()  # A JSON field to store multiple choice options
    answer = models.CharField(max_length=50)

    def get_videos(self):
        return [getattr(self, f'video_{i}') for i in range(1, 5)]

    def serialize(self):
        return {
            'type': 'idiom',
            'videos': [{'url': video.video_file.url, 'title': video.title} for video in self.get_videos()],
            'question': self.question,
            'options': json.loads(self.options),
            'answer': self.answer,
        }

class VocabularyExercise(BaseExercise):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='vocabulary_video')
    word_1 = models.CharField(max_length=50)
    question_1 = models.CharField(max_length=255)
    options_1 = models.JSONField()  # A JSON field to store multiple choice options
    answer = models.CharField(max_length=250)

    def get_videos(self):
        return [self.video]

    def serialize(self):
        return {
            'type': 'vocabulary',
            'videos': [{'url': self.video.video_file.url, 'title': self.video.title}],
            'word_1': self.word_1,
            'question_1': self.question_1,
            'options_1': json.loads(self.options_1),
            'answer': self.answer,
        }


class FillInTheBlankExercise(BaseExercise):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='FITBE_video')
    part_before_blank = models.CharField(max_length=250)
    part_after_blank = models.CharField(max_length=250)
    options = models.JSONField()
    answer = models.CharField(max_length=255)

    def get_videos(self):
        return [self.video]

    def serialize(self):
        return {
            'type': 'fill_in_the_blank',
            'videos': [{'url': self.video.video_file.url, 'title': self.video.title}],
            'options': json.loads(self.options),
            'answer': self.answer,
            'part_before_blank': self.part_before_blank,
            'part_after_blank': self.part_after_blank,
        }

class GuessTheTranslationOfTheWord(BaseExercise):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='get_the_traslation')
    options = models.JSONField()
    eng_word = models.CharField(max_length=255, default='')
    answer = models.CharField(max_length=255)

    def get_videos(self):
        return [self.video]

    def serialize(self):
        return {
            'type': 'guess_the_translation',
            'videos': [{'url': self.video.video_file.url, 'title': self.video.title}],
            'options': json.loads(self.options),
            'eng_word': self.eng_word,
            'answer': self.answer,
        }
