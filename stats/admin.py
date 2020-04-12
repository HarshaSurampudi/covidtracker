from django.contrib import admin

# Register your models here.
from .models import Entry
from .models import DailyStat

admin.site.register(Entry)
admin.site.register(DailyStat)