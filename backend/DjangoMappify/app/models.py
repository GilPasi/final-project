from django.db import models

# Create your models here.
class Employee(models.Model):
    # The next things are for the ilustration of the server-client infurstracture
    Employee = models.CharField(max_length=30)
    Department = models.CharField(max_length=200)