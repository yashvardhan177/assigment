# meme_generator_app/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Add a URL pattern for the home page (if using 'home' view)
    # path('upload_image/', views.upload_image, name='upload_image'),
    path('show/<int:pk>/', views.show_meme, name='show_meme'),
    path('share/<int:pk>/twitter/', views.share_on_twitter, name='share_on_twitter'),
    path('signup/', views.signup, name='signup'),
    path('meme/<int:pk>/share/', views.share_on_twitter, name='share_on_twitter'),
]
