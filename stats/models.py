from django.db import models

class Entry(models.Model):
	place = models.CharField(max_length=200) 
	total_cases = models.IntegerField(default=0)
	recovered = models.IntegerField(default=0)
	active = models.IntegerField(default=0)
	deaths = models.IntegerField(default=0)
	def asdict(self):
		return {self.place: self.total_cases}
	def __str__(self):
		return self.place

class DailyStat(models.Model):
	total= models.IntegerField(default=0)
	active= models.IntegerField(default=0)
	recovered= models.IntegerField(default=0)
	deaths= models.IntegerField(default=0)
	date=models.DateField()
	def __str__(self):
		return str(self.date)



