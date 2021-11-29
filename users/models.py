import uuid
from django.db import models
# Create your models here.


class Profile(models.Model):
    firstname = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    bills = models.ManyToManyField('Bill', blank=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @classmethod
    def create(cls, email, username, password):
        profile = cls(email=email, username=username, password=password)
        return profile

    def __str__(self):
        return self.username


class Bill(models.Model):
    bill_number = models.UUIDField(default=uuid.uuid4, unique=True,
                                   primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    products = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)

    @classmethod
    def create(cls, name, address, phone, email, products, price):
        bill = cls(name=name, address=address, phone=phone,
                   email=email, products=products, price=price)
        return bill

    def __str__(self):
        return str(self.bill_number)+"("+self.name+")"
