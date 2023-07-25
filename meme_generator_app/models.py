# meme_generator_app/models.py

from django.contrib.auth.models import User
from django.db import models

class MemeImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meme_images/')
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100, blank=True)
    caption3 = models.CharField(max_length=100, blank=True)
    font_color1 = models.CharField(max_length=7, default='#000000')
    font_color2 = models.CharField(max_length=7, default='#000000')
    font_color3 = models.CharField(max_length=7, default='#000000')
    background_color1 = models.CharField(max_length=7, default='#ffffff')
    background_color2 = models.CharField(max_length=7, default='#ffffff')
    background_color3 = models.CharField(max_length=7, default='#ffffff')
    caption1_position = models.CharField(max_length=10, default='top')
    caption2_position = models.CharField(max_length=10, default='bottom')
    caption3_position = models.CharField(max_length=10, default='center')
    generated_meme = models.ImageField(upload_to='generated_memes/', blank=True)
    crop_image = models.BooleanField(default=False)  # New field for cropping option
    resize_image = models.BooleanField(default=False)


def __str__(self):
        return f"MemeImage-{self.id} by {self.user.username}"
