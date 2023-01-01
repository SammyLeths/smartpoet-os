# Generated by Django 3.1.4 on 2020-12-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20201206_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('pending review', 'Pending Review'), ('draft', 'Draft')], default='pending review', max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('password protected', 'Password Protected')], default='public', max_length=255),
        ),
    ]
