# posts/models.py

from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from members.models import User
from django.core import validators
from django.core.exceptions import ValidationError

# Create your models here.

status_choices = [('published', 'Published'), ('pending review', 'Pending Review'), ('draft', 'Draft')]
visibility_choices = [('public', 'Public'), ('private', 'Private'), ('password protected', 'Password Protected')]



def validate_post_image(image):
    max_height = 640
    max_width = 1280
    height = image.height
    width = image.width
    if width != max_width or height != max_height:
        raise ValidationError("The accepted dimension for post image is Width - 1280px and Height - 640px")



class PostCategory(models.Model):

    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PostCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name






class PostSubCategory(models.Model):

    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, null=True, related_name="parentcategory")
    name = models.CharField(max_length=255, unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PostSubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name






class Post(models.Model):

    # ONE TO MANY RELATIONSHIP BETWEEN USER AND POST
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    heading = models.CharField(max_length=50, null=True, validators=[validators.MinLengthValidator(15)])
    intro = models.TextField(max_length=500, null=True, validators=[validators.MinLengthValidator(45)])
    title = models.CharField(max_length=75, null=True, unique=True, validators=[validators.MinLengthValidator(5)])
    slug = models.SlugField(max_length=75, null=True, validators=[validators.MinLengthValidator(5)])
    content = RichTextField(max_length=4000, null=True, validators=[validators.MinLengthValidator(45)])

    # ONE TO ONE RELATIONSHIP BETWEEN POST AND IT'S CATEGORY
    #category = models.OneToOneField(PostCategory, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(PostCategory, null=True, on_delete=models.SET_NULL)

    # ONE TO ONE RELATIONSHIP BETWEEN POST AND IT'S SUB CATEGORY
    #sub_category = models.OneToOneField(PostSubCategory, null=True, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(PostSubCategory, null=True, on_delete=models.SET_NULL)

    post_image = models.ImageField(null=True, blank=True, upload_to='images/post_images/', validators=[validate_post_image])
    status = models.CharField(max_length=255, choices=status_choices, default='pending review')
    visibility = models.CharField(max_length=255, choices=visibility_choices, default='public')
    notify = models.BooleanField(null=True, blank=True)
    agree = models.BooleanField(null=True)
    published_date = models.DateField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_user")
    bookmarks = models.ManyToManyField(User, blank=True, related_name="bookmarked_user")
    downvotes = models.ManyToManyField(User, blank=True, related_name="downvote_user")
    upvotes = models.ManyToManyField(User, blank=True, related_name="upvote_user")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

