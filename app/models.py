from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    number = models.IntegerField(null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=100,null=True)
    role = models.CharField(max_length=100,null=True)
    isProfileComplete = models.CharField(max_length=100,default='False')
    isActive = models.CharField(max_length=100,default='False')

class Clubs(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    clubName = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100,null=True)
    websites = models.CharField(max_length=100,null=True)
    licence = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to ='club_images',null=True)
    
class Sports(models.Model):
    club = models.ForeignKey(Clubs,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,default='False')
    description = models.CharField(max_length=100,default='False')
    fees = models.CharField(max_length=100,default='False')
    img = models.ImageField(upload_to ='sports_images',null=True)

class Members(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    EnrolledSports = models.ForeignKey(Sports,on_delete=models.CASCADE,null=True)
    isFeesPaid = models.CharField(max_length=100,default='False')
    dateOfPayment = models.DateField(null=True)
    dateOfEnroll = models.DateField(null=True)
    dateOfQuit = models.DateField(null=True)
    status = models.CharField(max_length=100,default='Active')

