from django.db import models
from djongo.models.fields import ObjectIdField, Field
from django.contrib.auth.models import User


class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_balance = models.FloatField(default=0)
    usd_balance = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    ips = Field(default=[])
    subprofiles = Field(default={})


ORDER_TYPE_CHOICES = (
    ('Buy', 'Buy'),
    ('Sell', 'Sell')
)

ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed')
)


class Order(models.Model):
    _id = ObjectIdField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    quantity = models.FloatField()
    quantity_left = models.FloatField()
    order_type = models.Field(
        max_length=4,
        choices=ORDER_TYPE_CHOICES
    )
    status = models.Field(
        max_length=9,
        choices=ORDER_STATUS_CHOICES,
        default='Pending'
    )
