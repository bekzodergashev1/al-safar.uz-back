from django.db.models import fields
from django_filters import FilterSet, NumberFilter, CharFilter, DateTimeFilter
from .models import Driver, Trip, Country, Province, District


class DriverFilter(FilterSet):
    pasport = CharFilter(field_name="pasport", lookup_expr="icontains")
    license = CharFilter(field_name="license", lookup_expr="icontains")

    class Meta:
        model = Driver
        fields = ["user", "smoking"]


class TripFilter(FilterSet):
    leave_time_from = DateTimeFilter(field_name="leave_time", lookup_expr='lte')
    leave_time_to = DateTimeFilter(field_name="leave_time", lookup_expr='gte')
    price_min = NumberFilter(field_name="price", lookup_expr="lte")
    price_max = NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = Trip
        fields = ['driver', 'From', 'To', 'car']


class CountryFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontaines')

    class Meta:
        model = Country
        fields = []


class ProvinceFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontaines')

    class Meta:
        model = Province
        fields = ['country']


class DistrictFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontaines')

    class Meta:
        model = District
        fields = ["province"]
