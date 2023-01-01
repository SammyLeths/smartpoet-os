# members/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db.models.deletion import CASCADE
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.

region_choices = [('africa', 'Africa'), ('antarctica', 'Antarctica'), ('asia', 'Asia'), ('australia', 'Australia'), ('europe', 'Europe'), ('north-america', 'North-America'), ('south-america', 'South-America')]

gender_choices = [('male', 'Male'), ('female', 'Female')]

role_choices = [('admin', 'Admin'), ('author', 'Author')]

status_choices = [('pending activation', 'Pending Activation'), ('active', 'Active'), ('inactive', 'Inactive')]


def validate_profile_image(image):
    max_height = 300
    max_width = 300
    height = image.height
    width = image.width
    if width != max_width or height != max_height:
        raise ValidationError("The accepted dimension for profile image is Width - 300px and Height - 300px")


def validate_profile_cover(image):
    max_height = 400
    max_width = 1280
    height = image.height
    width = image.width
    if width != max_width or height != max_height:
        raise ValidationError("The accepted dimension for cover image is Width - 1280px and Height - 400px")


class User(AbstractUser):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='first name')
    last_name = models.CharField(max_length=254, verbose_name='last name')
    email = models.EmailField(max_length=254, error_messages={'unique': 'A user with that email already exists.'},
                              unique=True, verbose_name='email address')
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/profile_pic/', validators=[validate_profile_image])
    cover_image = models.ImageField(null=True, blank=True, upload_to='images/profile_cover/', validators=[validate_profile_cover])
    birthday = models.DateField(null=True)
    phone_number = models.CharField(max_length=64, null=True)
    region = models.CharField(choices=region_choices, max_length=64, null=True)
    bio = models.TextField(null=True)
    occupation = models.CharField(max_length=255, null=True)
    gender = models.CharField(choices=gender_choices, max_length=64, null=True)
    religion = models.CharField(max_length=64, null=True)
    role = models.CharField(choices=role_choices, max_length=256, default='author')
    status = models.CharField(choices=status_choices, max_length=64, default='pending email verification')

    #####################################

    institution = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    program = models.CharField(max_length=255, null=True, blank=True)
    period = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    program_desc = models.TextField(null=True, blank=True)

    #####################################

    facebook = models.URLField(max_length=255, null=True, blank=True)
    instagram = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.username)

    def delete_user(self):
        return reverse("staff:delete-user", args=[self.uuid])


class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, blank=True, related_name="follower_user")
    following = models.ManyToManyField(User, blank=True, related_name="following_user")

    def __str__(self):
        return f"User: {self.user.username}"
