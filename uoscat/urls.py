
from django.contrib import admin
from django.urls import path, include
import postapp.views
import loginapp.views

# media 파일올리기 위한 url 설정
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',postapp.views.home, name='home'),
    path('newcat/',postapp.views.newcat, name="newcat"),
    path('detail/<int:num>',postapp.views.detail, name='detail'),
    path('feed/<int:num>',postapp.views.feed, name='feed'),
<<<<<<< HEAD
    path('vote/<int:num>',postapp.views.vote, name='vote'),
=======
    path('addhabitat/<int:num>',postapp.views.addhabitat, name='addhabitat'),
>>>>>>> dd0ef29e05c6403e78b83ef02aaf7c75532851c7
    path('login/',loginapp.views.login, name='login'),
    path('accounts/',include('allauth.urls')),
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
