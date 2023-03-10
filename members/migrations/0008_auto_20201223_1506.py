# Generated by Django 3.1.4 on 2020-12-23 14:06

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='images/profile_cover/', validators=[members.models.validate_profile_cover]),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='images/profile_pic/', validators=[members.models.validate_profile_image]),
        ),
    ]
