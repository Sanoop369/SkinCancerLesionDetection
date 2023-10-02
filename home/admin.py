from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(patient_details)
admin.site.register(patient_report)
admin.site.register(Location)
admin.site.register(doctor_master)