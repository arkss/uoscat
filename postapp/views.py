from django.shortcuts import render, redirect
from django.utils import timezone
from django.core import serializers

from .form import CatPost

from .models import Cat
# 메인화면
def home(request):
    cats=Cat.objects.all()
    context={
        'cats': cats,
    }
    return render(request, 'postapp/home.html',context)

# 새로운 고양이 추가
def newcat(request):
    if request.method == "POST":
        form = CatPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # 임시 위치
            post.habitat_x = 1.0
            post.habitat_y = 1.0
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
    print(habitats)
    # habitats_json = serializers.serialize('json', habitats)
    # habitats_json = [ {data.fields} for data,e in habitats_json]
    # print(habitats_json)
    # try:
    context={
        'cat': cat,
        'habitat_len': len(habitats),
        'pos': habitats,
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
