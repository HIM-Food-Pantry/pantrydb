"""Client Models"""
from djmoney.models.fields import MoneyField

from accounts.models import BaseProfile


class ClientProfile(BaseProfile):
    """Pantry client profile"""

    unemployment = MoneyField("Unemployment", max_digits=10, decimal_places=2, default_currency='USD')
    food_stamps = MoneyField("Food Stamps", max_digits=10, decimal_places=2, default_currency='USD')
    disability = MoneyField("Disability", max_digits=10, decimal_places=2, default_currency='USD')
    salary = MoneyField("Salary", max_digits=10, decimal_places=2, default_currency='USD')
    pension = MoneyField("Pension", max_digits=10, decimal_places=2, default_currency='USD')
    ss_ssi = MoneyField("Social and Supplemental Income", max_digits=10, decimal_places=2, default_currency='USD')
