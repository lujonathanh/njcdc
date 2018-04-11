from django.db import models

# Create your models here.

class Zipcode(models.Model):
    zipcode = models.IntegerField()
    population = models.IntegerField()
    persons_per_household = models.FloatField()
    average_house_value = models.FloatField()
    income_per_household = models.FloatField()
    electricity = models.FloatField()
    nat_gas = models.FloatField()
    fuel_oil = models.FloatField()
    vehic_miles_traveled = models.FloatField()
    transport = models.FloatField()
    housing = models.FloatField()
    food = models.FloatField()
    goods = models.FloatField()
    services = models.FloatField()
    total_household_footprint = models.FloatField()
    households_per_zipcode = models.IntegerField()
    total_zipcode_footprint = models.FloatField()
    
    def __str__(self):
        return str(self.zipcode) + " with footprint " +\
        	str(self.total_zipcode_footprint)