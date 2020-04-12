from django.core.management.base import BaseCommand
import requests
import pandas as pd
from stats.models import Entry

class Command(BaseCommand):
    help = 'Loads Data to DB'

    def handle(self, *args, **kwargs):
    	url = 'https://www.mohfw.gov.in/'
    	html = requests.get(url).content
    	df_list = pd.read_html(html)
    	df = df_list[-1]
    	df = df[:-2]
    	df.columns = ['serial', 'place' , 'total_cases', 'recovered', 'deaths']
    	Entry.objects.all().delete()
    	Entry.objects.bulk_create(
    		Entry(**vals) for vals in df.to_dict('records')
    		)