# Generated by Django 3.2.7 on 2021-09-09 10:45

import api.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mapbox_location_field.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='phone number')),
                ('image', models.ImageField(default='default-user.png', upload_to='user-images/')),
                ('gender', models.IntegerField(choices=[(1, 'Female'), (2, 'Male')], null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('type', models.IntegerField(choices=[(0, 'customer'), (1, 'driver')], null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=8, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.MaxLengthValidator(8)])),
                ('seats', models.PositiveSmallIntegerField()),
                ('type', models.IntegerField(choices=[(1, 'Car'), (2, 'Bus')], null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('air_conditioner', models.BooleanField(default=False)),
                ('color', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pasport', models.CharField(max_length=9, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(9)])),
                ('license', models.CharField(max_length=9, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(9)])),
                ('smoking', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_time', models.DateTimeField()),
                ('price', models.PositiveIntegerField()),
                ('From', models.ForeignKey(db_column='from', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.district', verbose_name='from')),
                ('To', models.ForeignKey(db_column='to', on_delete=django.db.models.deletion.DO_NOTHING, related_name='to', to='api.district', verbose_name='to')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.car')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.driver')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', mapbox_location_field.models.LocationField(map_attrs={'center': (41.30617455098567, 69.28421350980352), 'style': 'mapbox://styles/mapbox/navigation-night-v1'})),
                ('address', mapbox_location_field.models.AddressAutoHiddenField(map_id='map')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.district')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.country')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.province'),
        ),
    ]