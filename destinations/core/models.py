from django.db import models

# Create your models here.
class User(models.Model):
    name = models.TextField()
    email = models.TextField(unique=True)
    password_hash = models.TextField()

class Session(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, primary_key=True)
    token = models.TextField()

class Destination(models.Model):
    name = models.TextField()
    review = models.TextField()
    rating = models.PositiveIntegerField()
    share_publicly = models.BooleanField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)

