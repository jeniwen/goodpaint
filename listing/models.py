from django.db import models
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename

# Create your models here.
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    medium = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=20)
    image = models.ImageField(upload_to=get_upload_path)
    descrip = models.CharField(max_length=10000)
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
