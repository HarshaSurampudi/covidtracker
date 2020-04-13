from twilio.rest import Client
import time
import requests
from stats.models import PhoneNumber
from django.core.management.base import BaseCommand
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
class Command(BaseCommand):
    help = 'Sends wap stats'

    def handle(self, *args, **kwargs):
        account_sid = 'ACd6a11c43a774a9884c0753087a732dc4'
        auth_token = '09ff91b796470b143c673feaafe4ef8f'
        client = Client(account_sid, auth_token)
        url = 'https://api.covid19india.org/data.json'
        r = requests.get(url)
        data = r.json()
        state_data_with_total = data["statewise"]
        for item in state_data_with_total:
            if (item['state'] == "Total"):
                total_stat = item
                break
            else:
                total_stat = None
        text = "COVID-19 Statistics:- Total cases : "+str(total_stat["confirmed"])+", Active cases : " +str(total_stat["active"])+", Recovered Cases : "+str(total_stat["recovered"])+", Deceased : "+str(total_stat["deaths"])
        phone_list= PhoneNumber.objects.all()
        phone_set=set()
        for phone in phone_list:
            phone_set.add(phone.wap_number)
        for sms in client.messages.list():
            print(sms.to)

        for number in phone_set:
            message = client.messages.create(
                                          body=text,
                                          from_='whatsapp:+14155238886',
                                          to='whatsapp:'+str(number)
                                      )
            print(message.sid)
            time.sleep(5)
