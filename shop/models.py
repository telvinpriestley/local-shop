from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Items(models.Model):
    itemName = models.CharField(max_length=100)
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    contact = models.IntegerField()
    address = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(
        max_length=6,
        choices=[("Male", "Male"), ("Female", "Female")],
        null=True,
        blank=True,
    )

class Tempstore(models.Model):
    fname = models.CharField(max_length=200, blank=True, null=True)
    lname = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)

class PaymentMethod(models.Model):
    method = models.ForeignKey(Order, on_delete=models.CASCADE)
    pay_method = models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    card_number = models.IntegerField()
    cvv = models.IntegerField()
    exp_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Recipient(models.Model):
    recipient = models.ForeignKey(Order, on_delete=models.CASCADE)
    names = models.CharField(max_length=100)
    email  = models.CharField(max_length=100)
    ship_county = models.CharField(max_length=100, blank=True, null=True)
    ship_state = models.CharField(max_length=100, blank=True, null=True)
    ship_address = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class History(models.Model):
    payment = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    