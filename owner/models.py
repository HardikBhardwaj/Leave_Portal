from django.db import models

# Create your models here.



   
class Status(models.Model):
     name = models.CharField(max_length=200)
     sickleave = models.IntegerField(blank=True, null=True)
     casualleave=models.IntegerField(blank=True, null=True)
     optionalleave=models.IntegerField(blank=True, null=True)
     overday=models.CharField(max_length=300,blank=True, null=True)
     employ_id = models.CharField(max_length=200,null=True)
     joining_date = models.DateTimeField(null=True)

    


class AdminUser(models.Model):
     name=models.CharField(max_length=200)
     reason=models.CharField(max_length=300)
     from1 = models.DateTimeField()
     to = models.DateTimeField()
     status1=models.CharField(max_length=200)
     noofdays=models.CharField(max_length=300)

class optional(models.Model):
     optionalleave= models.DateTimeField(max_length=200)
     description=models.CharField(max_length=200)

class compulsary(models.Model):
     compulsaryleave= models.DateTimeField(max_length=200)
     description =models.CharField(max_length=200)
class Totalleave(models.Model):
    name=models.CharField(max_length=200)
    leaves=models.IntegerField(blank=True, null=True)
    sick_leave_alloted=models.IntegerField(blank=True, null=True)
class forgot(models.Model):
     name=models.CharField(max_length=200)
     otp=models.IntegerField(blank=True, null=True)