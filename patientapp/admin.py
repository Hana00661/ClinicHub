from django.contrib import admin
from patientapp import models

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'mobile', 'gender', 'date_of_birth', 'blood_group', 'address', 'image']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type', 'seen', 'date']


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Notification, NotificationAdmin)
