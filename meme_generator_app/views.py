

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .form import MemeImageForm
from .models import MemeImage
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import tweepy
from django.contrib.auth.views import LoginView
from django.conf import settings
import logging
import textwrap

# genrate meme function

def generate_meme(meme_image):
    # Load the image using Pillow (PIL)
    image_path = os.path.join(settings.MEDIA_ROOT, meme_image.image.name)
    image = Image.open(image_path)

    # Define font properties
    font_size = 40
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Calculate the position to draw each caption
    caption1_position = (50, 50)
    caption2_position = (50, image.height - 100)
    caption3_position = (image.width // 2, image.height // 2)

    # Draw the captions on the image
    draw.text(caption1_position, meme_image.caption1, fill=meme_image.font_color1, font=font, stroke_width=2, stroke_fill=meme_image.background_color1)
    draw.text(caption2_position, meme_image.caption2, fill=meme_image.font_color2, font=font, stroke_width=2, stroke_fill=meme_image.background_color2)
    draw.text(caption3_position, meme_image.caption3, fill=meme_image.font_color3, font=font, stroke_width=2, stroke_fill=meme_image.background_color3)

    # Create the 'generated_memes' folder if it doesn't exist
    generated_memes_folder = os.path.join(settings.MEDIA_ROOT, 'generated_memes')
    if not os.path.exists(generated_memes_folder):
        os.makedirs(generated_memes_folder)

    # Save the generated meme to the 'generated_memes' folder
    generated_meme_path = os.path.join(generated_memes_folder, f'meme_{meme_image.pk}.png')
    image.save(generated_meme_path)

    # Save the path of the generated meme to the MemeImage object
    meme_image.generated_meme.name = f'generated_memes/meme_{meme_image.pk}.png'
    meme_image.save()

def get_text_position(image, position, text_width, text_height):
    # Calculate the position to place the text based on the desired position
    img_width, img_height = image.size

    if position == 'top':
        x = (img_width - text_width) // 2
        y = 10
    elif position == 'bottom':
        x = (img_width - text_width) // 2
        y = img_height - text_height - 10
    else:  # 'center'
        x = (img_width - text_width) // 2
        y = (img_height - text_height) // 2

    return x, y

@login_required
def home(request):
    if request.method == 'POST':
        form = MemeImageForm(request.POST, request.FILES)
        if form.is_valid():
            meme_image = form.save(commit=False)
            meme_image.user = request.user
            meme_image.save()
            generate_meme(meme_image)  # Call the generate_meme function after saving the MemeImage object
            return redirect('show_meme', pk=meme_image.pk)  # Redirect to show_meme view after generating the meme
    else:
        form = MemeImageForm()
    return render(request, 'home.html', {'form': form})



def show_meme(request, pk):
    meme_image = get_object_or_404(MemeImage, pk=pk)

    # If the meme is not generated, generate it
    if not meme_image.generated_meme:
        generate_meme(meme_image)

    return render(request, 'show_meme.html', {'meme_image': meme_image})

def crop_image(image):
    return image

def resize_image(image):
    return image



def share_on_twitter(request, pk):
    meme_image = get_object_or_404(MemeImage, pk=pk)

    # Authenticate with Twitter
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Generate the message to be tweeted (you can customize this message)
    message = f"Check out this cool meme I created using Meme Generator! {meme_image.image.url}"

    try:
        # Upload the meme image to Twitter and post the tweet
        media = api.media_upload(meme_image.generated_meme.path)

        try:
            api.update_status(status=message, media_ids=[media.media_id])
            logger.info(f"Tweet successfully posted for MemeImage with id {meme_image.pk}")
        except tweepy.TweepError as e:
            logger.error(f"Error sharing on Twitter (TweepError) for MemeImage with id {meme_image.pk}: {str(e)}")
            return redirect('show_meme', pk=pk, error_message="Error sharing on Twitter. Please try again later.")
        except Exception as e:
            logger.error(f"Error sharing on Twitter (Other) for MemeImage with id {meme_image.pk}: {str(e)}")
            return redirect('show_meme', pk=pk, error_message="Error sharing on Twitter. Please try again later.")

    except tweepy.TweepError as e:
        # Handle Twitter API errors (e.g., rate limit exceeded, invalid credentials, etc.)
        logger.error(f"Error uploading media to Twitter for MemeImage with id {meme_image.pk}: {str(e)}")
        return redirect('show_meme', pk=pk, error_message="Error sharing on Twitter. Please try again later.")
    except Exception as e:
        # Handle other unexpected errors
        logger.error(f"Unexpected error while sharing on Twitter for MemeImage with id {meme_image.pk}: {str(e)}")
        return redirect('show_meme', pk=pk, error_message="Error sharing on Twitter. Please try again later.")

    return redirect('show_meme', pk=pk)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful sign-up
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('home')

