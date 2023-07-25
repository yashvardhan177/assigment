# meme_generator_app/forms.py

from django import forms
from .models import MemeImage

class MemeImageForm(forms.ModelForm):
    class Meta:
        model = MemeImage
        fields = ['caption1', 'font_color1', 'background_color1', 'caption1_position',
                  'caption2', 'font_color2', 'background_color2', 'caption2_position',
                  'caption3', 'font_color3', 'background_color3', 'caption3_position',
                  'image']
