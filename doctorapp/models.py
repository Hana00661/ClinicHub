from django.db import models
from django.utils import timezone
from userauthapp import models as userauth_models  # import the models from the userauthapp app ,userauth_models this is a just name and it can be anything

NOTIFICATION_TYPE = (
    ("New Appointment", "New Appointment"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)
class Doctor(models.Model):         #create a new model from scratch
    user = models.OneToOneField(userauth_models.User, on_delete=models.CASCADE)  #when we delete this user , we delete doctor, there should be only one doctor that has one user model
    image = models.FileField(upload_to='images', blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
                #i add blank=True, null=True just for the sake of production environment where i might need to automatically populate the doctor via a csv to prevent errors
                #in case the full name is not available
                #if i dont want to do that i can just remove the blank=True, null=True
    mobile = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    specializations = models.CharField(max_length=100, null=True, blank=True)
    qualifications = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.CharField(max_length=100, null=True, blank=True)
    next_available_appointment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.full_name}" #string representation for the doctor
class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True) #one doctor can have many notifications
    appointment = models.ForeignKey("mainapp.Appointment", on_delete=models.CASCADE, null=True, blank=True, related_name="doctor_appointment_notification") #one appointment can have many notifications
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notification"
    
    def __str__(self):
        return f"Dr {self.doctor.full_name} Notification"