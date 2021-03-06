from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth import logout
from .form import CatPost
import json
import datetime

from django.views.decorators.csrf import csrf_exempt #csrf 귀찮아.



from .models import Cat,Choice, Vote, Comment, CatImage
# 소셜 로그인 User 불러오기
from django.contrib.auth.models import User

# 메인화면
def home(request):
    cats=Cat.objects.all()
    paginator = Paginator(cats, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    # User test
    # if request.user.is_authenticated:
    #     print(request.user.id)
    #     print(get_object_or_404(User,pk=request.user.pk))
    context={
        'cats': cats,
        'posts': posts,
        'now': 'home',
    }
    return render(request, 'postapp/home.html',context)

from django.views.generic.edit import FormView
from .form import CatPost
"""
class FileFieldView(FormView):
    form_class = CatPost
    template_name = 'postapp/create_edit.html'
    success_url = ''  

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                pass
            return self.form_valid(form)
        else:
            return self.form_invalid(form)  
"""
# 새로운 고양이 추가
def newcat(request):
    req_type=request_post_and_authenticated(request)

    if req_type==1:
        form = CatPost(request.POST, request.FILES)
        
        if form.is_valid():
            cat = Cat()
            cat.name = form.cleaned_data['name']
            cat.image = form.cleaned_data['image']
            
            cat.gender = form.cleaned_data['gender']
            cat.lasteat = timezone.now()
            cat.body = form.cleaned_data['body']
            cat.user=get_object_or_404(User,pk=request.user.pk)
            cat.save()
            files = request.FILES.getlist('image')
            for f in files:
                catimage = CatImage(cat=cat, sub_image=f)
                catimage.save()
        return redirect('home')

        # return render(request, 'postapp/home.html')

    else:
        form = CatPost()
        context={
            'form':form,
            'now':'new',
            'writing':True,
        }
        return render(request, 'postapp/create_edit.html',context)

# 각 고양이의 상세페이지
def detail(request,cat_id):
    cat=Cat.objects.get(id=cat_id)
    habitats=[pos.as_dict() for pos in cat.habitat_set.all()]

    # vote가 없을 경우 예외 처리
    try:
        vote = Vote.objects.get(cat_id=cat_id)

    except: # vote를 시작한 사람을 고양이 등록자로 선정할 필요가 있을까 싶지만 일단 고!
        vote = Vote(cat_id=cat_id,user=get_object_or_404(User,pk=request.user.pk))
        vote.save()
    # 해당 고양이의 vote 의 id 에 일치하는 고양이 후보이름만 가져온다.
    choices = Choice.objects.filter(vote_id=cat.vote.id)

    choices_name = [choice.as_dict() for choice in choices]

    max_count = 0
    for choice in choices:
        if max_count < choice.count:
            max_count = choice.count
    # filter를 통해서 투표수가 제일 많은 choice객체들을 모두 불러온다.
    max_name = Choice.objects.filter(vote_id=cat.vote.id, count = max_count)
    max_name = [name.as_dict() for name in max_name]

    context={
        'cat': cat,
        'choices': choices,
        'choices_exist': len(choices)>0,
        'choices_name': choices_name,
        'vote': vote,
        'habitat_len': len(habitats),
        'pos': habitats,
        'now': 'detail',
        'max_name': max_name,
        'own': cat.user.pk==request.user.pk, #글작성자와 로그인한 유저가 같은가?
    }
    return render(request,'postapp/detail.html',context)



def add_habitat(request,cat_id):
    req_type=request_post_and_authenticated(request)
    if req_type==1:
        cat=Cat.objects.get(pk=cat_id)
        position_string=request.POST['position_string'].split('&')
        position=[e.split(',') for e in position_string][:-1]
        for xy in position:
            cat.habitat_set.create(x=float(xy[0]),y=float(xy[1]))
        # print(cat.habitat_set.all())
    return redirect('detail',str(cat_id))

# 고양이의 이름 투표 기능
def vote_condition(request,cat_id):
    cat = Cat.objects.get(id=cat_id)
    req_type=request_post_and_authenticated(request)
    # 투표를 종료하면 기존의 이름도 데이터에서 삭제해준다. 나중에는 그냥 투표자체를 없애는 걸로 바꾸자.
    if cat.voting and req_type==1:
        cat.voting = False
        # 투표를 종료하면 고양이의 이름을 투표의 1등으로 바꿔준다.
        choices = Choice.objects.filter(vote_id=cat.vote.id)
        max_count = 0
        for choice in choices:
            if max_count < choice.count:
                max_count = choice.count
        # filter를 통해서 투표수가 제일 많은 choice객체들을 모두 불러온다.
        new_name = Choice.objects.filter(vote_id=cat.vote.id, count = max_count)

        # 그 객체가 1개 이상일 경우에는 값을 저장하지 않고 redirect 시킨다.
        if (len(new_name) > 1):
            return redirect('/detail/'+str(cat.pk))

        cat.name = new_name[0].as_str()

        vote = Vote.objects.get(cat_id=cat.id).delete()

    # 투표를 시작하면 voting을 True로 바꿔주고 현재 고양이의 이름도 투표 목록에 넣어준다.
    else:
        cat.voting = True
        #origin name 삭제. 이미 newcat에서 만들어줬음.

    # choices = Choice.objects.all()
    cat.save()
    return redirect('/detail/'+str(cat.pk))

@csrf_exempt
def vote(request, vote_id):
    vote = Vote.objects.get(pk=vote_id)
    selection = request.POST['choice']

    choice = Choice.objects.get(vote_id=vote_id, id=selection)
    choice.count += 1
    choice.save()

    return redirect('/detail/'+str(vote.cat.id))


# 마지막으로 밥 준 시간
def feed(request,cat_id):
    cat=Cat.objects.get(id=cat_id)
    cat.lasteat=timezone.now()
    cat.save()
    return redirect('/detail/'+str(cat.id))


# 새로운 이름 투표에 이름 추가해주기
@csrf_exempt
def add_name(request, cat_id):
    cat = Cat.objects.get(id = cat_id)
    choice = Choice(vote_id = cat.vote.id, count=0,user=get_object_or_404(User,pk=request.user.pk))
    choice_all = Choice.objects.filter(vote_id=cat.vote.id)
    # 입력 시 공백문자를 무시하고 가져온다.
    choice.name = request.POST['add_name'].strip()

    # 투표에 이름 추가시 같은 이름 있을 경우 추가 안되게 하기
    # 기존의 같은 이름이 있는지 확인해준다. 해당 투표에 선택받을 수 있는 이름을 다가져와 이를 순회하면서 입력 받은 값과 같으면 값을 저장하지 않고 redirect 시킨다.
    for choice_one in choice_all:
        # type(choice_one) 은 <class 'postapp.models.Choice'>
        # type(choice.name) 은 <class 'str'> 이어서 형변환을 시켜서 비교해주었다.
        # 입력한 이름의 길이가 0일 경우(위에서 화이트 스페이스를 모두 제거 해주었으므로 화이트스페이스로만 입력하면 무조건 길이가 0이다.) 예외처리해준다.
        if str(choice_one) == choice.name or len(choice.name) == 0:
            return redirect('/detail/'+str(cat.id))

    choice.save()
    return redirect('/detail/'+str(cat.id))

# 고양이 글 삭제

def delete(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    cat.delete()
    return redirect('/')

# 고양이 글 수정

def edit(request, cat_id):
    cat = Cat.objects.get(id=cat_id)

    req_type = request_post_and_authenticated(request)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if req_type==1:
        form = CatPost(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            cat.name = form.cleaned_data['name']
            cat.image = form.cleaned_data['image']
            cat.gender = form.cleaned_data['gender']
            cat.body = form.cleaned_data['body']
            cat.save()
            return redirect('/detail/'+str(cat.pk))

    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    elif req_type==2:
        form = CatPost(instance = cat)
        context={
            'form':form,
            'writing':True,
            'now':'edit',
        }
        return render(request, 'postapp/create_edit.html',context)
    else:
        return redirect('home')

# 투표 이름 삭제
def delete_choice(request, cat_id, choice_id):
    cat = Cat.objects.get(id=cat_id)
    choice = Choice.objects.get(vote_id=cat.vote.id, id=choice_id)
    choice.delete()
    return redirect('/detail/'+str(cat.id))

# 댓글 등록
def comment_write(request, cat_id):
    req_type=request_post_and_authenticated(request)
    if req_type==1:
        cat = get_object_or_404(Cat, pk=cat_id)
        content = request.POST.get('content')
        Comment.objects.create(cat=cat, comment_contents=content,user=get_object_or_404(User,pk=request.user.pk))
        return redirect('/detail/'+str(cat.id))
    return render(request, 'postapp/home.html')

# 댓글 삭제
def comment_delete(request, cat_id, comment_id):
    cat = Cat.objects.get(id=cat_id)
    comment = Comment.objects.get(id=comment_id)
    if comment.user.pk == request.user.pk:
        comment.delete()
    return redirect('/detail/'+str(cat.id))


# POST 메소드 & 사용자는 로그인 상태 : 1
# POST 메소드 x & 사용자는 로그인 상태 : 2
# POST 메소드x & 사용자 로그인 x : 0
def request_post_and_authenticated(request):
    if request.method == "POST" and request.user.is_authenticated:
        return 1
    elif request.user.is_authenticated:
        return 2
    return 0
