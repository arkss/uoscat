
from django.contrib import admin
from django.urls import path
import postapp.views

# media 파일올리기 위한 url 설정
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',postapp.views.home, name='home'),
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
