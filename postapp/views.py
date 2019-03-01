from django.shortcuts import render

# 메인화면
def home(request):
    return render(request, 'postapp/home.html')

# 새로운 고양이 추가
def create(request):
    return 

# 각 고양이의 상세페이지
def detail(request):
    return

# 고양이의 이름 투표 기능
def vote(request):
    return 

# 마지막으로 밥 준 시간 
def feed(request):
    return 


