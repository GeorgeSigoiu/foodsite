import uuid
from django.db import models


# Create your models here.


class Bill(models.Model):
    class Builder:
        def set_address(self, address):
            self.address = address
            return self

        def set_name(self, name):
            self.name = name
            return self

        def set_phone(self, phone):
            self.phone = phone
            return self

        def set_email(self, email):
            self.email = email
            return self

        def set_products(self, products):
            self.products = products
            return self

        def set_price(self, price):
            self.price = price
            return self

        def build(self):
            return Bill.createInstance(self)

    bill_number = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    products = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @classmethod
    def createInstance(cls, builder):
        bill = cls(name=builder.name,
                   address=builder.address,
                   phone=builder.phone,
                   email=builder.email,
                   products=builder.products,
                   price=builder.price)
        return bill

    def __str__(self):
        return str(self.created_at)[:19] + " - " + str(self.bill_number)[:6]


class Profile(models.Model):
    class Builder:
        firstname = surname = email = phone = address = ""

        def set_firstname(self, firstname):
            self.firstname = firstname
            return self

        def set_surname(self, surname):
            self.surname = surname
            return self

        def set_email(self, email):
            self.email = email
            return self

        def set_username(self, username):
            self.username = username
            return self

        def set_password(self, password):
            self.password = password
            return self

        def set_phone(self, phone):
            self.phone = phone
            return self

        def set_address(self, address):
            self.address = address
            return self

        def build(self):
            return Profile.createInstance(self)

    firstname = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    bills = models.ManyToManyField('Bill', blank=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    @classmethod
    def createInstance(cls, builder):
        profile = cls(username=str(builder.username),
                      surname=str(builder.surname),
                      firstname=str(builder.firstname),
                      password=str(builder.password),
                      phone=str(builder.phone),
                      address=str(builder.address),
                      email=str(builder.email))
        return profile

    def __str__(self):
        return self.username
