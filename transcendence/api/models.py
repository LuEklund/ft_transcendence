import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from .imageValidation import validateFileType, validationImageSize, defineNameImage
from django.core.files import File


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not username:
            raise ValueError(_('Users must have a username'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('coallition', 'foragers')
        file = open("app/static/images/profileIconWhite.png", "rb")
        djangoFile = File(file)
        extra_fields.setdefault('avatarImage', djangoFile)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)






class CustomUserData(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    onlineStatus = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)
    coallition = models.CharField()
    avatarImage = models.FileField(upload_to=defineNameImage, validators=[validationImageSize, validateFileType], blank=True)

    objects = CustomUserManager()

    def get_coallition(self):
        return self.coallition

    def __str__(self):
        return self.username

class Players(models.Model):
    name = models.CharField(max_length=255)

class Tournament(models.Model):
    STATE_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Active'),
        ('F', 'Finished'),
    ]

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField()
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    sate = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    players = models.ManyToManyField(Players, related_name='tournaments')
