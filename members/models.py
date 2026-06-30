#models are shaped similarly to classes in OOP, so they can also have their own methods.
from django.db import models

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)

class Tuff(models.Model):
    username = models.CharField(max_length=100)
    
    def hello_self(self):
        return "I am the " + self.username
    