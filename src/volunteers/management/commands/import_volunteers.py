"""Import Volunteers from CSV"""
import csv
import os

from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from ._generate_username import generate_username

from volunteers.models import VolunteerProfile

script_dir = os.path.dirname(__file__)

abs_file_path = os.path.join(script_dir, 'Volunteers.csv')

volunteers = open(abs_file_path, "rU")

data = csv.DictReader(volunteers)


class Command(BaseCommand):
    """Import Volunteers from CSV"""

    help = 'Import Volunteers from CSV'

    def handle(self, **options):
        for row in data:
            email = row['Email']
            first_name = row['First Name'],
            last_name = row['Last Name'],
            username = generate_username(first_name, last_name)
            print(username)
            user = User.objects.create_user(
                username.replace(" ", ""),
                email.lower(),
                User.objects.make_random_password()
            )
            user.first_name = row['First Name'].lower()
            user.last_name = row['Last Name'].lower()
            user.is_staff = False
            user.active = row['Active']
            user.save()
            volunteer_group = Group.objects.get_or_create(name="volunteers")
            volunteer_group[0].user_set.add(user)

            volunteer_profile = VolunteerProfile(
                user=user,
                organization=row['Organization'],
                house_number_street_name=row['Address'],
                state=row['State'].lower(),
                city=row['City'].lower(),
                zip_code=row['Zip Code'],
                interview=bool(row['Interview']),
                daytime_phone_number=row['Daytime Phone'],
                home_phone_number=row['Home Phone'],
                cell_phone_number=row['Cell Phone'],
                emergency_contact=row['Emergency Contact'],
                days_available=row['Days Available'],
                food_pantry=bool(row['Food Pantry']),
                bi_lingual=bool(row['Biligual']),
                fund_raising=bool(row['Fund Raising']),
                board_member=bool(row['Board']),
                sunshine_committee=bool(row['Sunshine Committe']),
                solicit_donations=bool(row['Solicit Donations']),
                record_keeping=bool(row['Record Keeping']),
                truck_or_van=bool(row['Truck or Van']),
                pick_up_food=bool(row['Pickup food']),
                deliver_food=bool(row['Deliver Food'])
            )

            volunteer_profile.save()
            # user.comments = row['Comments']
            # user.drivers_licence = row['Drivers Licence Number']
            # user.unemployment = row['Unemployment']
            # user.food_stamps = row['Food Stamps']
            # user.disability = row['Disability']
            # user.salary = row['Salary']
            # user.pension = row['Pension']
            # user.ss_ssi = row['Social and Supplemental Income']
