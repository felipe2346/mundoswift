from django.contrib import admin

from .models import Shipment, CountryLocation, LiveUpdate

admin.site.register(Shipment)
admin.site.register(LiveUpdate)
admin.site.register(CountryLocation)
