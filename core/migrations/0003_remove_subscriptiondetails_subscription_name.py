# Generated by Django 4.1.7 on 2023-03-06 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_subscriptiondetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptiondetails',
            name='subscription_name',
        ),
    ]