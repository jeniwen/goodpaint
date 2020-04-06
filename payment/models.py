from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    name = models.CharField("Full name",max_length=1024)
    address1 = models.CharField("Address line 1",max_length=1024)
    address2 = models.CharField("Address line 2",max_length=1024,blank=True)
    city = models.CharField("City", max_length=1024)
    province = models.CharField("State/Province/Region", max_length=30)
    postal_code = models.CharField("ZIP / Postal code",max_length=12)
    country = models.CharField("Country",max_length=20)

    def __str__(self):
        return self.name + "\n " + self.address1 + "\n " + self.address2




# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id
