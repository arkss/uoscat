from django.contrib import admin

from .models import Cat, Vote, Choice,Habitat, Comment


admin.site.register(Cat)
admin.site.register(Vote)
admin.site.register(Choice)
admin.site.register(Habitat)
admin.site.register(Comment)

