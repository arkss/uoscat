from django.contrib import admin
from .models import Cat, Vote, Choice

admin.site.register(Cat)
admin.site.register(Vote)
admin.site.register(Choice)
