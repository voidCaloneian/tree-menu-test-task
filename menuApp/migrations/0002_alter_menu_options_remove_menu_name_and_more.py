# Generated by Django 4.1.3 on 2023-03-06 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menuApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ('id',)},
        ),
        migrations.RemoveField(
            model_name='menu',
            name='name',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='order',
        ),
    ]