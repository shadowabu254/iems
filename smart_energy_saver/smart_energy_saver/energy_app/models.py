from django.db import models
from django.contrib.auth.models import User

class EnergyConsumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    energy_used = models.FloatField()  # kWh

class CarbonFootprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    carbon_saved = models.FloatField()  # CO2 saved in kg

class EnergyTip(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title