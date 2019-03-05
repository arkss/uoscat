
from django.contrib import admin
from django.urls import path
import postapp.views

# media 파일올리기 위한 url 설정
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',postapp.views.home, name='home'),
    path('create/',postapp.views.create, name='create'),
    path('detail/<int:num>',postapp.views.detail, name='detail'),
    path('feed/<int:num>',postapp.views.feed, name='feed')

] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
