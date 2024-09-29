from django.urls import path
from mainapp import views

app_name = "mainapp"        # This sets the namespace

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
]