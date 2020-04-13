from django.http import HttpResponse
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
            return redirect(index)
    else:
        form = Subscribe()
    phone_list= PhoneNumber.objects.all()
    phone_set=set()
    for phone in phone_list:
        phone_set.add(phone.wap_number)
    available_count= 250-len(phone_set)
    available_flag= 250>len(phone_set)
    template=loader.get_template('stats/subscribe_wap.html')
    context={'form': form, 'available_count': available_count,'available_flag':available_flag }
    return HttpResponse(template.render(context, request))
