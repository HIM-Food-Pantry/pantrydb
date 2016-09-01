import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from volunteers.models import VolunteerLog

User = get_user_model()
default_password = User.objects.make_random_password()


def generate_username(first_name, last_name):
    val = "{0}{1}".format(first_name[0], last_name[0]).lower()
    x = 0
    while True:
        if x == 0 and User.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}{1}".format(val, x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val
        x += 1
        if x > 1000000:
            raise Exception("Name is super popular!")


members = open('./scripts/volunteer_signin_log.csv', "rU")
data = csv.DictReader(members)

for row in data:
    first_name = row['First Name']
    last_name = row['Last Name']
    try:
        user = User.objects.get(first_name=first_name, last_name=last_name)
    except ObjectDoesNotExist:
        username = generate_username(first_name, last_name)
        user = User.objects.create_user(username, default_password)
    except MultipleObjectsReturned:
        user = User.objects.get(first_name=first_name, last_name=last_name)[0]
    print(first_name, last_name)
    # date = input(row['Date'])
    # now convert the string into datetime object given the pattern
    date = datetime.strptime(row['Date'], '%m/%d/%y')
    # print the datetime in any format you wish. It must be in YYYY-MM-DD format.
    # %Y Year with century as a decimal number.
    # %m Month as a zero-padded decimal number.
    # %d Day of the month as zero-padded decimal number
    volunteer_log = VolunteerLog.objects.create(
        user_id=user.id,
        date=date.strftime('%Y-%m-%d'),
        hours_worked=row['Hours Worked']
    )
    volunteer_log.save()
