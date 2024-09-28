from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
import requests
import stripe

from mainapp import models as base_models
from doctorapp import models as doctor_models
from patientapp import models as patient_models

def index(request):
    services = base_models.Service.objects.all()
    context = {
        "services": services
    }
    return render(request, "mainapp/index.html", context)

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    context = {
        "service": service
    }
    return render(request, "mainapp/service_detail.html", context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # Update patient bio data
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        patient.save()

        # Create appointment object
        base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
        )

    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    return render(request, "mainapp/book_appointment.html", context)