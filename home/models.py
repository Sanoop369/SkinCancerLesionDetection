from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model


# Create your models here.


class Location(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class patient_details(models.Model):
    
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
   
   
    gender = models.CharField(max_length=50)
    addr = models.CharField(max_length=500)
    location=models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=150)
    contact = models.CharField(max_length=50)
    username =models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.fname
    
class patient_report(models.Model):
    patient=models.ForeignKey(patient_details,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="skin_images",null=True)
    result = models.CharField(max_length=150)
    time=models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,default="You have No Problem.You are Healthy.No need of any Doctor Consulting")
    def __str__(self):
        return f"{self.patient.fname} 's Report"


class doctor_master(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    d_descp = models.CharField(max_length=500)
    d_qualification = models.CharField(max_length=500)
    d_category = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    image=models.ImageField(upload_to="doctor",null=True)
    location=models.ForeignKey(Location,on_delete=models.CASCADE)
    def __str__(self):
        return self.fname