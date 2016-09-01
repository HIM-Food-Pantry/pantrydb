from django.contrib.auth.models import User

default_password = User.objects.make_random_password()


def generate_username(first_name, last_name):
    """Accepts a first and last name to generate incrementing user_names"""
    first_last_name = "{0}{1}".format(first_name, last_name).lower()
    x = 0
    while True:
        if x == 0 and User.objects.filter(username=first_last_name).count() == 0:
            return first_last_name.lower()
        else:
            new_val = "{0}{1}".format(first_last_name, x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val.lower()
        x += 1
        if x > 1000000:
            raise Exception("Name is super popular!")
