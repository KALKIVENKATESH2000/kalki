from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name  

class Product(models.Model):
    CATEGORIES = (
        ('out door', 'Out Door'),
        ('indoor', 'Indoor'),
        ('fashion', 'Fashion'),
        ('mobiles', 'Mobiles'),
    )
    name = models.CharField(max_length=50)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    discripotion = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('out of delevery', 'Out of Delevery'),
        ('delivered' , 'Delivered'),
    )
    customer = models.ForeignKey("Customer", null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey("Product", null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.product.name