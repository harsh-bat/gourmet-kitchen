from django.db import models
from django.contrib.auth.models import User
from .storage import OverwriteStorage
import time
# Create your models here.
class Everyone(models.Model):
    def user_directory_path_dp(instance, filename):
        return 'kitchen/{0}/{1}'.format('dp', str(instance.id.email+str(time.time())))
    def user_directory_path_cover(instance, filename):
        return 'kitchen/{0}/{1}'.format('cover', str(instance.id.email+str(time.time())))
    id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    about = models.CharField(max_length=5000, null=True)
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(default=0)
    dp = models.FileField(upload_to=user_directory_path_dp,null=True, storage=OverwriteStorage())
    cover = models.FileField(upload_to=user_directory_path_cover,null=True, storage=OverwriteStorage())
    type = models.CharField(max_length=1)

class Recipe(models.Model):
    def user_directory_path_rec(instance, filename):
        return 'kitchen/{0}/{1}'.format('rec', str(instance.rec_id+str(time.time())))
    rec_id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    dir = models.CharField(max_length=10000)
    cal = models.IntegerField(default=0)
    time_hr = models.IntegerField(default=0)
    time_min = models.IntegerField(default=0)
    rec_img = models.FileField(upload_to=user_directory_path_rec,null=True, storage=OverwriteStorage())
    ingredients = models.CharField(max_length=16)
