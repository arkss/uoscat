from django.db import models
# from django.utils import timezone
import django.utils.timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Cat(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images')
    image_thumbnail = ImageSpecField(source='image',processors=[ResizeToFill(500,500)],format='BMP')
    gender = models.CharField(choices=[("male","수컷"),("female","암컷"),("null","모름")],max_length=20)
    body = models.TextField(blank=True)
    lasteat = models.DateTimeField(blank=True)
    voting = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CatImage(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.cat.name + "image"

class Vote(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    cat = models.OneToOneField(Cat,on_delete=models.CASCADE)

    def __str__(self):
        return self.cat.name+"의 투표"

class Choice(models.Model):
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {'name':self.name}

    def as_str(self):
        return self.name

class Habitat(models.Model):
    x=models.FloatField(blank=False)
    y=models.FloatField(blank=False)
    cat=models.ForeignKey(Cat,on_delete=models.CASCADE)

    def __str__(self):
        return "(%.5f,%.5f)"%(self.x,self.y)

    def as_dict(self):
        return {'x':self.x,'y':self.y}

class Comment(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)
    comment_date =models.DateTimeField(auto_now_add=True) # add_now_add 는 등록시 현재시간으로 추가함
    comment_contents = models.CharField(max_length=200)
     
    def __str__(self):
        return self.comment_contents