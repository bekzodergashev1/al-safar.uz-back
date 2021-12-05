from rest_framework import routers
from api.views import DriversViewSet, StationViewSet, TripViewSet, CountryViewSet, ProvinceViewSet, DistrictViewSet, \
    RegisterAPI

router = routers.DefaultRouter()
router.register("drivers", DriversViewSet, basename="drivers"),
router.register("stations", StationViewSet, basename="stations"),
router.register("trips", TripViewSet, basename="trips"),
router.register("countries", CountryViewSet, basename="countries"),
router.register("province", ProvinceViewSet, basename="province"),
router.register("district", DistrictViewSet, basename="district"),
router.register("register", RegisterAPI, basename="register"),

