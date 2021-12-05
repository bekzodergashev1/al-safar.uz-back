from django.db.models import fields
from rest_framework.serializers import *
from rest_framework.utils import field_mapping
from .models import Driver, User, Trip, Car
from .models import Country, Province, District, Station
from rest_framework import serializers
from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])

        return user


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', "last_name", "phone", "image", "gender", "type"]


class DriverSerializerGET(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = "__all__"
        depth = 1


class DriverSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


# ---------------------------------------------

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class ProvinceSerializerGET(ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"
        depth = 1


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class DistrictSerializerGET(ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"
        depth = 2


class StationSerializer(ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class StationSerializerGET(ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"
        depth = 3


# ------------------------------------------------

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class TripSerializerGET(ModelSerializer):
    driver = DriverSerializerGET()

    class Meta:
        model = Trip
        fields = "__all__"
        depth = 3
