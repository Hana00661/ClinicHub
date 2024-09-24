from django.contrib import admin
from doctorapp import models

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specializations', 'qualifications', 'years_of_experience']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']

admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Notification, NotificationAdmin)