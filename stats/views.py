from django.http import HttpResponse
from twilio.rest import Client
from django.template import loader
from django.shortcuts import redirect
from .forms import Subscribe
from .models import PhoneNumber
import requests

def index(request):
    url = 'https://api.covid19india.org/data.json'
    r = requests.get(url)
    data = r.json()
    state_data_with_total = data["statewise"]
    state_data= [d for d in state_data_with_total if d.get('state') != "Total"]
    for item in state_data_with_total:
        if (item['state'] == "Total"):
            total_stat = item
            break
        else:
            total_stat = None
    cases_time_series=data["cases_time_series"]
    for d in cases_time_series:
        d["totalconfirmed"] = int(d["totalconfirmed"])
        d["totaldeceased"]=int(d["totaldeceased"])
        d["totalrecovered"]=int(d["totalrecovered"])
        d["totalactive"]=d["totalconfirmed"]-d["totaldeceased"]-d["totalrecovered"]
    #print(cases_time_series)
    template = loader.get_template('stats/stats.html')
    #total_stat = Entry.objects.get(place="Total")
    context = { 'state_data': state_data, 'total_stat': total_stat,'cases_time_series':cases_time_series, }
    return HttpResponse(template.render(context, request))

def subscribeWap(request):
    if request.method == 'POST':
        form = Subscribe(request.POST)
        if form.is_valid():
            cleaned_data= form.cleaned_data
            if(not PhoneNumber.objects.filter(wap_number=cleaned_data["phoneNumber"])):
                phoneNumber=PhoneNumber()
                phoneNumber.wap_number=cleaned_data["phoneNumber"]
                phoneNumber.save()
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
                message = client.messages.create(
                                              body=text,
                                              from_='whatsapp:+14155238886',
                                              to='whatsapp:'+str(phoneNumber.wap_number)
                                          )

            return redirect(index)
    else:
        form = Subscribe()
    phone_list= PhoneNumber.objects.all()
    phone_set=set()
    for phone in phone_list:
        phone_set.add(phone.wap_number)
    available_count= 900-len(phone_set)
    available_flag= 900>len(phone_set)
    template=loader.get_template('stats/subscribe_wap.html')
    context={'form': form, 'available_count': available_count,'available_flag':available_flag }
    return HttpResponse(template.render(context, request))
