# Generated by Django 4.2.3 on 2023-07-24 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_generator_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memeimage',
            name='generated_meme',
            field=models.ImageField(blank=True, upload_to='generated_memes/'),
        ),
    ]
