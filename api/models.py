from typing import ClassVar
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator
from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from mapbox_location_field.models import LocationField, AddressAutoHiddenField
from .validators import DriverValidator, PasportIdValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        self.phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = None
    phone = PhoneNumberField(_('phone number'), unique=True)
    image = ImageField(upload_to="user-images/", default="default-user.png")
    gender = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], choices=(
        (1, "Female"),
        (2, "Male")
    ), null=True)
    type = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], choices=(
        (0, "customer"),
        (1, "driver")
    ), null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone)


class Driver(Model):
    user = OneToOneField(User, on_delete=CASCADE, validators=[DriverValidator()])
    pasport = CharField(max_length=9, validators=[MinLengthValidator(9), MaxLengthValidator(9), PasportIdValidator()])
    license = CharField(max_length=9, validators=[MinLengthValidator(9), MaxLengthValidator(9)])
    smoking = BooleanField(default=False)

    def __str__(self):
        return str(self.user.phone)


class Car(Model):
    name = CharField(max_length=255)
    number = CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    seats = PositiveSmallIntegerField()

    type = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], choices=(
        (1, "Car"),
        (2, "Bus"),
    ), null=True)
    air_conditioner = BooleanField(default=False)
    color = CharField(max_length=60)

    def __str__(self) -> str:
        return f"{self.name} - {self.number} - {self.color}"


class Country(Model):
    name = CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Province(Model):
    name = CharField(max_length=255)
    country = ForeignKey(Country, on_delete=DO_NOTHING)

    def __str__(self) -> str:
        return self.name


class District(Model):
    name = CharField(max_length=255)
    province = ForeignKey(Province, on_delete=DO_NOTHING)

    def __str__(self) -> str:
        return self.name


class Station(Model):
    name = CharField(max_length=255)
    district = ForeignKey(District, on_delete=DO_NOTHING)
    location = LocationField(
        map_attrs={"style": "mapbox://styles/mapbox/navigation-night-v1", "center": (41.306, 69.284)})
    address = AddressAutoHiddenField()

    def __str__(self) -> str:
        return self.name


class Trip(Model):
    driver = ForeignKey(Driver, on_delete=DO_NOTHING)
    From = ForeignKey(District, on_delete=DO_NOTHING, related_name="+", verbose_name="from", db_column='from')
    To = ForeignKey(District, on_delete=DO_NOTHING, related_name="to", verbose_name="to", db_column='to')
    car = ForeignKey(Car, on_delete=DO_NOTHING)
    leave_time = DateTimeField()
    users = ManyToManyField(User)
    price = PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.driver.user.phone} - {self.car.name}"
