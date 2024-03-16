from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserScore(models.Model):
    engTest = models.IntegerField(null=True, blank=True)
    aptest = models.IntegerField(null=True, blank=True)
    selfTest = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    low = models.IntegerField(null=True, blank=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)