# Generated by Django 4.2.5 on 2023-11-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0009_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='profile_pic',
            field=models.ImageField(default='Profile_Pics/Default_Profile_Pic.png', upload_to='Profile_Pics'),
        ),
    ]
