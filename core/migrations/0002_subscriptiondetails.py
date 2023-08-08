# Generated by Django 4.1.7 on 2023-03-06 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=100)),
                ('subscription_status', models.CharField(max_length=20)),
                ('subscription_amount', models.IntegerField()),
                ('subscription_name', models.CharField(max_length=100)),
                ('subscription_period', models.CharField(max_length=100, null=True)),
                ('subscription_start_date', models.DateTimeField()),
                ('subscription_end_date', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscrition_details_api', to='core.customer')),
            ],
        ),
    ]
