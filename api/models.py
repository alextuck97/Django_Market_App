from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class User(AbstractUser):
    balance = models.FloatField(default=10000.0)


class Stocks(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=5)
    quantity = models.IntegerField()
    date_last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.owner) + str(self.symbol)


class PortfolioHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_assets = models.FloatField()
    cash_assets = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return str(self.owner) + str(self.date)