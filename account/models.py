import string
import random
from django.db import models
from . import constants
from geopy.geocoders import Nominatim

class Shipment(models.Model):
    sender_name = models.CharField(max_length=150)
    sender_email = models.EmailField(null=True, blank=True)
    sender_phone = models.CharField(max_length=20, null=True, blank=True)
    sender_address = models.CharField(max_length=200, null=True, blank=True)

    receiver_name = models.CharField(max_length=150)
    receiver_email = models.EmailField(null=True, blank=True)
    receiver_phone = models.CharField(max_length=20, null=True, blank=True)
    receiver_address = models.CharField(max_length=200, null=True, blank=True)

    tracking_number = models.CharField(max_length=100, unique=True, blank=True)
    weight = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    shipping_type = models.CharField(max_length=100)
    origin_office = models.CharField(max_length=100)
    destination_office = models.CharField(max_length=100)
    # shipping_date = models.DateField()
    # delivery_date = models.DateField()
    # booking_mode = models.CharField(max_length=100)
    # amount_paid = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.sender_name

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_unique_tracking_number()
        super().save(*args, **kwargs)

    def generate_unique_tracking_number(self, length=12):
        characters = string.ascii_uppercase + string.digits
        while True:
            tracking_number = ''.join(random.choices(characters, k=length))
            if not Shipment.objects.filter(tracking_number=tracking_number).exists():
                return tracking_number


class CountryLocation(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def save(self, *args, **kwargs):
        self.country_name = self.country_name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.country_name


class LiveUpdate(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='live_update', on_delete=models.CASCADE)
    # country = models.CharField(max_length=150)
    # country_ref = models.ForeignKey(CountryLocation, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(CountryLocation, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=150)
    remark = models.CharField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    stages_status = models.CharField(max_length=50, choices=constants.STATES_LIVE_CHOICES)
    stages_label = models.CharField(max_length=50, choices=constants.STATES_LABEL_CHOICES)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # If country is set and lat/lng missing, get from country
        if self.country:
            self.latitude = self.country.latitude
            self.longitude = self.country.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        return self.status
