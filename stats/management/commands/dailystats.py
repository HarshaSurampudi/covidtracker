from django.core.management.base import BaseCommand
import requests
import pandas as pd
from stats.models import Entry
from stats.models import DailyStat
import datetime

class Command(BaseCommand):
    help = 'loads daily stats'

    def handle(self, *args, **kwargs):
        all_entries= Entry.objects.all()
        grand_total=0
        grand_deaths=0
        grand_recovered=0
        for entry in all_entries:
            grand_total+=entry.total_cases
            grand_recovered+=entry.recovered
            grand_deaths+=entry.deaths
        grand_active = grand_total - grand_recovered - grand_deaths
        ds=DailyStat()
        ds.total=grand_total
        ds.active=grand_active
        ds.recovered=grand_recovered
        ds.deaths=grand_deaths
        ds.date=datetime.date.today()
        ds.save()

