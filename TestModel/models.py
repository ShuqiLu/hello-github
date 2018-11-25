from django.db import models
class Test(models.Model):
	person1= models.CharField(max_length=20)
	person2=models.CharField(max_length=20) 
	newid=models.CharField(max_length=20)
class news(models.Model):
	title= models.CharField(max_length=20)
	context=models.CharField(max_length=20)
# Create your models here.
