from contextvars import Token

from django.contrib.auth import authenticate, logout, login
from django.db.models import query
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .responses import ResponseSuccess, ResponseFail
from .serializers import DriverSerializerGET, DriverSerializer, StationSerializer, StationSerializerGET, TripSerializer, \
    TripSerializerGET, CountrySerializer, ProvinceSerializer, ProvinceSerializerGET, DistrictSerializer, \
    DistrictSerializerGET
from .models import Driver, Station, Trip, Country, Province, District
from .filters import DriverFilter, TripFilter, CountryFilter, ProvinceFilter, DistrictFilter
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer


# Register API
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginView(APIView):

    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")
        user = authenticate(phone=phone, password=password)
        if user:
            serializer = UserSerializer(user, many=False)
            login(request, user=user)
            token, created = Token.objects.get_or_create(user=user)
            return ResponseSuccess({"token": token.key, "user": serializer.data})
        else:
            return ResponseFail({
                "errors": "Phone number or password not correct"
            })


class LogoutView(APIView):
    permission_classes = IsAuthenticated

    def delete(self, request):
        logout(request)


# Create your views here.

def get_object_or_None(model, pk: int):
    try:
        return model.objects.get(id=pk)
    except:
        return None


class DriversViewSet(ViewSet):
    def __init__(self, **kwargs) -> None:
        self.MODEL = Driver
        self.SERIALIZERGET = DriverSerializerGET
        self.SERIALIZER = DriverSerializer
        self.FILTER = DriverFilter
        self.FILTER_FIELDS = [
            "user",
            "passport",
            "license",
            "smoking",
        ]
        super().__init__(**kwargs)

    def list(self, request):
        queryset = self.MODEL.objects.all()
        filter = self.FILTER(request.GET, queryset=queryset)
        queryset = filter.qs
        serializer = self.SERIALIZERGET(queryset, many=True)
        return ResponseSuccess(serializer.data, filter_fields=self.FILTER_FIELDS)

    def create(self, request):
        serializer = self.SERIALIZER(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrieve(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZERGET(query, many=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("The ID you sent is incorrect")

    def update(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZER(data=request.data, instance=query)
            if serializer.is_valid():
                serializer.save()
                return ResponseSuccess(serializer.data)
            else:
                return ResponseFail("Invalid data")
        else:
            return ResponseFail("The ID you sent is incorrect")

    def destroy(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            query.delete()
            return ResponseSuccess("Deleted object")
        else:
            return ResponseFail("The ID you sent is incorrect")


class StationViewSet(ViewSet):
    def __init__(self, **kwargs) -> None:
        self.MODEL = Station
        self.SERIALIZERGET = StationSerializerGET
        self.SERIALIZER = StationSerializer
        # self.FILTER = DriverFilter
        # self.FILTER_FIELDS = [
        #     "user",
        #     "passport",
        #     "license",
        #     "smoking",
        # ]
        super().__init__(**kwargs)

    def list(self, request):
        queryset = self.MODEL.objects.all()
        # filter = self.FILTER(request.GET, queryset=queryset)
        # queryset = filter.qs
        serializer = self.SERIALIZERGET(queryset, many=True)
        return ResponseSuccess(serializer.data)  # , filter_fields=self.FILTER_FIELDS)

    def create(self, request):
        serializer = self.SERIALIZER(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrieve(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZERGET(query, many=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("The ID you sent is incorrect")

    def update(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZER(data=request.data, instance=query)
            if serializer.is_valid():
                serializer.save()
                return ResponseSuccess(serializer.data)
            else:
                return ResponseFail("Invalid data")
        else:
            return ResponseFail("The ID you sent is incorrect")

    def destroy(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            query.delete()
            return ResponseSuccess("Deleted object")
        else:
            return ResponseFail("The ID you sent is incorrect")


class TripViewSet(ViewSet):
    def __init__(self, **kwargs) -> None:
        self.MODEL = Trip
        self.SERIALIZER = TripSerializer
        self.SERIALIZERGET = TripSerializerGET
        self.FILTER = TripFilter
        self.FILTER_FIELDS = [
            "driver",
            "From",
            "To",
            "car",
            "price_min",
            "price_max",
            "leave_time_from",
            "leave_time_to",
        ]
        super().__init__(**kwargs)

    def list(self, request):
        queryset = self.MODEL.objects.all()
        filter = self.FILTER(request.GET, queryset=queryset)
        queryset = filter.qs

        serializers = self.SERIALIZERGET(queryset, many=True)
        return ResponseSuccess(serializers.data)

    def create(self, request):
        serializer = self.SERIALIZER(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrive(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZERGET(query, mant=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("The ID you send is incorrect")

    def update(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZER(data=request.data, instance=query)
            if serializer.is_valid():
                serializer.save()
            else:
                return ResponseFail("Invalid data")
        else:
            return ResponseFail("The ID you send is incorrect")


class CountryViewSet(ViewSet):
    def __init__(self, **kwargs) -> None:
        self.MODEL = Country
        self.SERIALIZER = CountrySerializer
        self.SERIALIZERGET = CountrySerializer
        self.FILTER = CountryFilter
        self.FILTER_FIELDS = [
            "name"
        ]
        super().__init__(**kwargs)

    def list(self, request):
        queryset = self.MODEL.objects.all()
        filter = self.FILTER(request.GET, queryset=queryset)
        queryset = filter.qs

        serializers = self.SERIALIZERGET(queryset, many=True)
        return ResponseSuccess(serializers.data)

    def create(self, request):
        serializer = self.SERIALIZER(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrive(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZERGET(query, mant=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("The ID you send is incorrect")

    def update(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZER(data=request.data, instance=query)
            if serializer.is_valid():
                serializer.save()
            else:
                return ResponseFail("Invalid data")
        else:
            return ResponseFail("The ID you send is incorrect")


class ProvinceViewSet(ViewSet):
    def __init__(self, **kwargs) -> None:
        self.MODEL = Province
        self.SERIALIZER = ProvinceSerializer
        self.SERIALIZERGET = ProvinceSerializerGET
        self.FILTER = ProvinceFilter
        self.FILTER_FIELDS = [
            "name",
            "country"
        ]
        super().__init__(**kwargs)

    def list(self, request):
        queryset = self.MODEL.objects.all()
        filter = self.FILTER(request.GET, queryset=queryset)
        queryset = filter.qs

        serializers = self.SERIALIZERGET(queryset, many=True)
        return ResponseSuccess(serializers.data)

    def create(self, request):
        serializer = self.SERIALIZER(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrive(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZERGET(query, mant=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("The ID you send is incorrect")

    def update(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZER(data=request.data, instance=query)
            if serializer.is_valid():
                serializer.save()
            else:
                return ResponseFail("Invalid data")
        else:
            return ResponseFail("The ID you send is incorrect")


class DistrictViewSet(ViewSet):
    def __init__(self, **kwargs) -> None:
        self.MODEL = District
        self.SERIALIZER = DistrictSerializer
        self.SERIALIZERGET = DistrictSerializerGET
        self.FILTER = DistrictFilter
        self.FILTER_FIELDS = [
            "name",
            "province",
        ]
        super().__init__(**kwargs)

    def list(self, request):
        queryset = self.MODEL.objects.all()
        filter = self.FILTER(request.GET, queryset=queryset)
        queryset = filter.qs

        serializers = self.SERIALIZERGET(queryset, many=True)
        return ResponseSuccess(serializers.data)

    def create(self, request):
        serializer = self.SERIALIZER(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrive(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZERGET(query, mant=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("The ID you send is incorrect")

    def update(self, request, pk):
        query = get_object_or_None(self.MODEL, pk)
        if query:
            serializer = self.SERIALIZER(data=request.data, instance=query)
            if serializer.is_valid():
                serializer.save()
            else:
                return ResponseFail("Invalid data")
        else:
            return ResponseFail("The ID you send is incorrect")
