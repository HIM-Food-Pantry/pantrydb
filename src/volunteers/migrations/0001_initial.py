# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 18:45
from __future__ import unicode_literals

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('sign_in_time', models.DateTimeField()),
                ('sign_out_time', models.DateTimeField(blank=True, null=True)),
                ('total_volunteer_time', models.DurationField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VolunteerProfile',
            fields=[
                ('user',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to=settings.AUTH_USER_MODEL)),
                ('daytime_phone_number',
                 phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True,
                                                                verbose_name='Daytime Phone Number')),
                ('home_phone_number',
                 phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True,
                                                                verbose_name='Home Phone Number')),
                ('cell_phone_number',
                 phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True,
                                                                verbose_name='Cell Number')),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Zip Code')),
                ('state', models.CharField(blank=True, max_length=20, null=True, verbose_name='State')),
                ('house_number_street_name',
                 models.CharField(blank=True, max_length=20, null=True, verbose_name='House Number Street Name')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='City')),
                ('organization', models.CharField(blank=True, max_length=200, null=True, verbose_name='Organization')),
                ('emergency_contact',
                 models.CharField(blank=True, max_length=200, null=True, verbose_name='Emergency Contact')),
                ('days_available',
                 models.CharField(blank=True, max_length=200, null=True, verbose_name='Days Available')),
                ('food_pantry', models.BooleanField(default=False, verbose_name='Food Pantry')),
                ('interview', models.BooleanField(default=False, verbose_name='Interview')),
                ('bi_lingual', models.BooleanField(default=False, verbose_name='Bi Lingual')),
                ('fund_raising', models.BooleanField(default=False, verbose_name='Fund Raising')),
                ('board_member', models.BooleanField(default=False, verbose_name='Board Member')),
                ('sunshine_committee', models.BooleanField(default=False, verbose_name='Sunshine Committee')),
                ('solicit_donations', models.BooleanField(default=False, verbose_name='Solicit Donations')),
                ('record_keeping', models.BooleanField(default=False, verbose_name='Record Keeping')),
                ('truck_or_van', models.BooleanField(default=False, verbose_name='Truck or Van')),
                ('pick_up_food', models.BooleanField(default=False, verbose_name='Pick up Food')),
                ('deliver_food', models.BooleanField(default=False, verbose_name='Deliver Food')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='volunteerlog',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
