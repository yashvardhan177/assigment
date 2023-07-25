# meme_generator_project/urls.py

from django.contrib import admin
from django.urls import path, include
from meme_generator_app.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),  # Use CustomLoginView for login
    path('meme/', include('meme_generator_app.urls')),
]


if settings.DEBUG:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)