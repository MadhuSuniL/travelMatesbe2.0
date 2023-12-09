from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from helper.Choices import MOTHER_TONGUES
from helper.Validators import phone_regex
from django.core.validators import EmailValidator
from helper.Funtions import Print
from .manager import TravelMateManager
from django.conf import settings
import os


class TravelMate(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    travel_mate_id = models.CharField(unique=True,max_length=255)
    profile_pic = models.FileField(null=True,upload_to='profiles')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True,validators=[EmailValidator])
    contry_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=10,unique=True,validators=[phone_regex])
    bio = models.CharField(max_length=30,default='-')
    date_of_birth = models.DateField(null=True)
    mother_tongue = models.CharField(max_length=20, choices=MOTHER_TONGUES,null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    trips = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

    groups = None
    user_permissions = None

    objects = TravelMateManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','first_name', 'last_name','contry_code']

    def __str__(self):
        return self.phone
            
    def save(self, *args, **kwargs):
        if not self.profile_pic:
            default_image_path = os.path.join(settings.STATIC_ROOT, 'default/profile/image.png')
            if os.path.exists(default_image_path):
                self.profile_pic.save('default_profile_image.png', open(default_image_path, 'rb'), save=True)
            else:
                pass                
        super().save(*args, **kwargs)
    
