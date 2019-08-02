from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User




class Ware(models.Model):
    name_ware = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    publish_on = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='pics')
    about = models.TextField()
    location = models.TextField()
    duration = models.CharField(max_length=200)
    price = models.IntegerField()
    insurance = models.IntegerField(help_text="hint:insurance non refundable")
   
    



    def __str__(self):
        return self.name_ware

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)

    genders = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    gender = models.CharField(max_length=1, choices=genders)

    def __str__(self):
        return self.user.username        

