import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    bills = models.ManyToManyField('Bill', blank=True)

    def __str__(self):
        return self.username


class Bill(models.Model):
    bill_number = models.UUIDField(default=uuid.uuid4, unique=True,
                                   primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    content_description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.bill_number+"("+self.name+")"
