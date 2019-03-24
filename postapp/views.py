from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth import logout
from .form import CatPost

from .models import Cat,Choice, Vote
# 메인화면
def home(request):
    cats=Cat.objects.all()
    paginator = Paginator(cats, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context={
        'cats': cats,
        'posts': posts,
        'now': 'home',
    }
    return render(request, 'postapp/home.html',context)

# 새로운 고양이 추가
def newcat(request):
    if request.method == "POST":
        form = CatPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.lasteat = timezone.now()
            post.save()
            return redirect('home')
        # return render(request, 'postapp/home.html')

    else:
        form = CatPost()
        return render(request, 'postapp/create.html',{'form':form})

# 각 고양이의 상세페이지
def detail(request,num):
    cat=Cat.objects.get(pk=num)
    habitats=[pos.as_dict() for pos in cat.habitat_set.all()]
    # vote가 없을 경우 예외 처리
    try:
        vote = Vote.objects.get(cat_id=num)

    except:
        vote = Vote(cat_id=num)
        vote.save()
    # 해당 고양이의 vote 의 id 에 일치하는 고양이 후보이름만 가져온다.
    choices = Choice.objects.filter(vote_id=cat.vote.id)

    context={
        'cat': cat,
        'choices': choices,
        'vote': vote,
        'habitat_len': len(habitats),
        'pos': habitats,
        'now': 'detail',
    }
    return render(request,'postapp/detail.html',context)



def addhabitat(request,num):
    if request.method == 'POST':
        cat=Cat.objects.get(pk=num)
        position_string=request.POST['position_string'].split('&')
        position=[e.split(',') for e in position_string][:-1]
        for xy in position:
            cat.habitat_set.create(x=float(xy[0]),y=float(xy[1]))
        # print(cat.habitat_set.all())
    return redirect('detail',str(num))

# 고양이의 이름 투표 기능
def vote_condition(request,num):
    cat = Cat.objects.get(pk=num)

    # 투표중인지 표시

    # 투표를 종료하면 기존의 이름도 데이터에서 삭제해준다. 나중에는 그냥 투표자체를 없애는 걸로 바꾸자.
    if cat.voting:
        cat.voting = False
        # 투표를 종료하면 고양이의 이름을 투표의 1등으로 바꿔준다.
        choices = Choice.objects.filter(vote_id=cat.vote.id)
        max_count = 0
        for choice in choices:
            if max_count < choice.count:
                max_count = choice.count
        # filter를 통해서 투표수가 제일 많은 choice객체들을 모두 불러온다.
        new_name = Choice.objects.filter(count = max_count)
        # 그 객체가 1개 이상일 경우에는 값을 저장하지 않고 redirect 시킨다.
        if (len(new_name) > 1):
            return redirect('/detail/'+str(cat.pk))

        cat.name = str(new_name)

        vote = Vote.objects.get(cat_id=cat.id).delete()

        

    # 투표를 시작하면 voting을 True로 바꿔주고 현재 고양이의 이름도 투표 목록에 넣어준다.
    else:
        cat.voting = True
        origin_name = Choice(vote_id=cat.vote.id, name=cat.name, count = 0)
        origin_name.save()

    # choices = Choice.objects.all()
    cat.save()
    return redirect('/detail/'+str(cat.pk))


def vote(request, vote_id):

    # cat = Cat.objects.get(pk=cat_id)
    vote = Vote.objects.get(pk=vote_id)
    # 이따 프론트에서 이 값으로 투표할 이름을 가져오게끔 하자.
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(vote_id=vote_id, id=selection)
        choice.count += 1
        choice.save()
    except:
        choice = Choice(vote_id=vote_id, name=selection, count=1)
        choice.save()

    return redirect('/detail/'+str(vote.cat.id))


# 마지막으로 밥 준 시간
def feed(request,num):
    cat=Cat.objects.get(pk=num)
    cat.lasteat=timezone.now()
    cat.save()
    return redirect('/detail/'+str(cat.pk))


# 새로운 이름 투표에 이름 추가해주기
def add_name(request, cat_id):
    cat = Cat.objects.get(id = cat_id)
    choice = Choice(vote_id = cat.vote.id)
    choice_all = Choice.objects.filter(vote_id=cat.vote.id)
    # 입력 시 공백문자를 무시하고 가져온다.
    choice.name = request.GET['add_name'].strip()
    
    # 투표에 이름 추가시 같은 이름 있을 경우 추가 안되게 하기
    # 기존의 같은 이름이 있는지 확인해준다. 해당 투표에 선택받을 수 있는 이름을 다가져와 이를 순회하면서 입력 받은 값과 같으면 값을 저장하지 않고 redirect 시킨다.
    for choice_one in choice_all:
        # type(choice_one) 은 <class 'postapp.models.Choice'>
        # type(choice.name) 은 <class 'str'> 이어서 형변환을 시켜서 비교해주었다.
        # 입력한 이름의 길이가 0일 경우(위에서 화이트 스페이스를 모두 제거 해주었으므로 화이트스페이스로만 입력하면 무조건 길이가 0이다.) 예외처리해준다.
        if str(choice_one) == choice.name or len(choice.name) == 0:
            return redirect('/detail/'+str(cat.pk))
    choice.count = 0
    choice.save()
    return redirect('/detail/'+str(cat.pk))

# 고양이 글 삭제

def delete(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    cat.delete()
    return redirect('/')

# 고양이 글 수정

def edit(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
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
    else:
        form = CatPost()
        return render(request, 'postapp/edit_post.html',{'form':form})

    
