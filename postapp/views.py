from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Cat
# 메인화면
def home(request):
    cats=Cat.objects.all()
    context={
        'cats': cats,
    }
    return render(request, 'postapp/home.html',context)

# 새로운 고양이 추가
def create(request):
    return

# 각 고양이의 상세페이지
def detail(request,num):
    cat=Cat.objects.get(pk=num)
    context={
        'cat': cat,
    }
    return render(request,'postapp/detail.html',context)

# 고양이의 이름 투표 기능
def vote(request):
    return

# 마지막으로 밥 준 시간
def feed(request,num):
    cat=Cat.objects.get(pk=num)
    cat.lasteat=timezone.now()
    cat.save()
    return redirect('/detail/'+str(cat.pk))
