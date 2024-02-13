from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    Gender_Choice=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    email = models.EmailField(unique=True)
    department=models.CharField(max_length=200, null=True)
    username=models.CharField(max_length=200, null=True)
    full_name=models.CharField(max_length=200, null=True)
    gender=models.CharField(max_length=7, choices=Gender_Choice)
    matric=models.CharField(max_length=10, unique=True, null=True)
    image =models.ImageField(default="default.jpg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img=Image.open(self.image.path)

        if img.height >300 and img.width > 300:
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)