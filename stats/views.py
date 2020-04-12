from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import requests
from .models import Entry

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

def loadData(request):
	url = 'https://api.covid19india.org/data.json'
	r = requests.get(url)
	data = r.json()
	all_state_data = data["statewise"]
	Entry.objects.all().delete()
	for state_data in all_state_data:
		print(state_data["state"]+" : "+ state_data["confirmed"])
		entry=Entry()
		entry.place=str(state_data["state"])
		entry.total_cases=int(state_data["confirmed"])
		entry.active=int(state_data["active"])
		entry.recovered=int(state_data["recovered"])
		entry.deaths=int(state_data["deaths"])
		entry.save()
	return redirect(index)