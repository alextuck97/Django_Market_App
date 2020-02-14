from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Stocks(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=5)
    
    watched_since = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.owner) + str(self.symbol)


