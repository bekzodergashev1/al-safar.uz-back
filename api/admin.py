from django.contrib import admin
from .models import *
from mapbox_location_field.admin import MapAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Station, MapAdmin)
admin.site.register(Car)
admin.site.register(Trip)