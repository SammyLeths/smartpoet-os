# Generated by Django 3.1.4 on 2020-12-07 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20201206_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postsubcategory',
            name='cat_id',
        ),
        migrations.AddField(
            model_name='postsubcategory',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.postcategory'),
        ),
    ]
