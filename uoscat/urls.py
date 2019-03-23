
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
    path('detail/<int:cat_id>/delete',postapp.views.delete, name='delete'), # 글 삭제
    path('detail/<int:cat_id>/edit', postapp.views.edit, name='edit'), # 글 수정
    path('feed/<int:num>',postapp.views.feed, name='feed'),
    path('votecondition/<int:num>',postapp.views.vote_condition, name='vote_condition'),
    path('vote/<int:vote_id>', postapp.views.vote, name='vote'),
    path('addname/<int:cat_id>', postapp.views.add_name, name='add_name'),
    path('vote/<int:num>',postapp.views.vote, name='vote'),
    path('addhabitat/<int:num>',postapp.views.addhabitat, name='addhabitat'),
    path('login/',loginapp.views.login, name='login'),
    path('accounts/',include('allauth.urls')),
   
    path('my_logout/',loginapp.views.my_logout,name='logout' ),
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# url(r'^login/$','django.contrib.auth.views.login', {'template_name': '/login.html'}), 