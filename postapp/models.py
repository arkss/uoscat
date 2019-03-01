from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images')
    gender = models.CharField(choices=[("male","수컷"),("female","암컷"),("null","모름")],max_length=20)
    habitat_x = models.FloatField()
    habitat_y = models.FloatField()
    body = models.TextField()
    lasteat = models.DateTimeField()

    def __str__(self):
        return self.name