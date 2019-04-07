
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
    # path('newcat/',postapp.views.FileFieldView.as_view(), name="newcat"),
    path('detail/<int:cat_id>',postapp.views.detail, name='detail'),
    path('detail/<int:cat_id>/delete',postapp.views.delete, name='delete'), # 글 삭제
    path('detail/<int:cat_id>/delete/<int:choice_id>', postapp.views.delete_choice, name='delete_choice'), # 이름 후보 삭제
    path('detail/<int:cat_id>/edit', postapp.views.edit, name='edit'), # 글 수정
    path('detail/<int:cat_id>/commentwrite', postapp.views.comment_write, name="comment_write"), # 댓글작성
    path('detail/<int:cat_id>/commentdelete/<int:comment_id>', postapp.views.comment_delete, name="comment_delete"), # 댓글삭제
    path('feed/<int:cat_id>',postapp.views.feed, name='feed'),
    path('votecondition/<int:cat_id>',postapp.views.vote_condition, name='vote_condition'), # 투표 상태
    path('vote/<int:vote_id>', postapp.views.vote, name='vote'), # 투표하기
    path('addname/<int:cat_id>', postapp.views.add_name, name='add_name'),
    path('addhabitat/<int:cat_id>',postapp.views.add_habitat, name='addhabitat'),

    # 로그인 및 로그아웃
    path('accounts/',include('allauth.urls')),
    path('login/',loginapp.views.login, name='login'),
    path('my_logout/',loginapp.views.my_logout,name='logout' ),
    
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# url(r'^login/$','django.contrib.auth.views.login', {'template_name': '/login.html'}),
