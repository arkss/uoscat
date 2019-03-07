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
    habitat_x = models.FloatField()
    habitat_y = models.FloatField()
    body = models.TextField(blank=True)
    lasteat = models.DateTimeField(blank=True)
    voting = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Vote(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    cat = models.OneToOneField(Cat,on_delete=models.CASCADE)

    def __str__(self):
        return self.cat.name

class Choice(models.Model):
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name



# class Poll(models.Model):
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     area = models.CharField(max_length = 15)

# class Choice(models.Model):
#     poll = models.ForeignKey(Poll) #Poll 모델의 id를 이용
#     candidate = models.ForeignKey(Candidate)
#     votes = models.IntegerField(default = 0)
