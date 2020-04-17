from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_gt_zero(value):
    if value <= 0:
        raise ValidationError(
            ('Value must be greater than zero.'),
            params={'value': value},
        )

def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename

# Create your models here.
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    medium = models.CharField(max_length=50)
    dimensions1 = models.DecimalField(max_digits=5, decimal_places=2)
    dimensions2 = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=7)
    image = models.ImageField(upload_to=get_upload_path)
    descrip = models.CharField(max_length=10000)
    stock = models.IntegerField(validators=[validate_gt_zero])
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.owner.username + " " + self.title

class ListingEdit(models.Model):
    title = models.CharField(max_length=140)
    descrip = models.CharField(max_length=10000)
    # image = models.ImageField(upload_to=get_upload_path)
    stock = models.IntegerField(validators=[validate_gt_zero])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
