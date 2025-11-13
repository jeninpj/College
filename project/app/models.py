from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    coursename=models.CharField(max_length=255) 
    fees=models.IntegerField(null=True)
    
class Student(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    studentname=models.CharField(max_length=255)
    address=models.CharField(max_length=255) 
    age=models.IntegerField()
    joiningdate=models.DateField()

class Teacher(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255) 
    age=models.IntegerField()
    phone=models.CharField(max_length=10,null=True)
    image=models.ImageField(upload_to='image/', null=True)
    