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
    # habitat_x = models.FloatField(default=37.5839)
    # habitat_y = models.FloatField(default=127.0588)
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

# <<<<<<< HEAD


# class Poll(models.Model):
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     area = models.CharField(max_length = 15)

# class Choice(models.Model):
#     poll = models.ForeignKey(Poll) #Poll 모델의 id를 이용
#     candidate = models.ForeignKey(Candidate)
#     votes = models.IntegerField(default = 0)
# =======
class Habitat(models.Model):
    x=models.FloatField(blank=False)
    y=models.FloatField(blank=False)
    cat=models.ForeignKey(Cat,on_delete=models.CASCADE)

    def __str__(self):
        return "(%.5f,%.5f)"%(self.x,self.y)

    def as_dict(self):
        return {'x':self.x,'y':self.y}
# >>>>>>> dd0ef29e05c6403e78b83ef02aaf7c75532851c7
