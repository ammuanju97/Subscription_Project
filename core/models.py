from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)

class SubscriptionDetails(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE,related_name='user_subscrition_details_api')
    product_id = models.CharField(max_length=100)
    subscription_status = models.CharField(max_length=20)
    subscription_amount = models.IntegerField()
    # subscription_name = models.CharField(max_length=100)
    subscription_period = models.CharField(max_length=100,null=True)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()
    # def __str__(self):
    #     return self.user.user