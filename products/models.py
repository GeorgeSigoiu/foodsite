from django.db import models
import uuid
# Create your models here.


class Product(models.Model):
    # owner = models.ForeignKey(
    #     Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    typeof = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    content = models.ManyToManyField('Content', blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title


class Content(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    typeof = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name+"("+self.typeof+")"


class Drink(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    price = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Sauce(models.Model):
    name = models.CharField(max_length=200)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    price = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
