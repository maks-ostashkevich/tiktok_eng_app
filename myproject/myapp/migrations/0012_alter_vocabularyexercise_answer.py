# Generated by Django 5.0.6 on 2024-06-29 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_rename_answer_1_vocabularyexercise_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabularyexercise',
            name='answer',
            field=models.CharField(max_length=250),
        ),
    ]