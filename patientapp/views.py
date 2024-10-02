from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from mainapp import models as base_models
from patientapp import models as patient_models


@login_required
def dashboard(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)
    
    context = {
        'appointments': appointments,
        'notifications': notifications,
        }

    return render(request, "patientapp/dashboard.html", context)



@login_required
def appointments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)

    context = {
        "appointments": appointments,
    }

    return render(request, "patientapp/appointments.html", context)


@login_required
def appointment_detail(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        "appointment": appointment,
        "medical_records": medical_records,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }

    return render(request, "patientapp/appointment_detail.html", context)




@login_required
def cancel_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)

    appointment.status = "Cancelled"
    appointment.save()

    messages.success(request, "Appointment Cancelled Successfully")
    return redirect("patientapp:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)

    appointment.status = "Scheduled"
    appointment.save()

    messages.success(request, "Appointment Re-Scheduled Successfully")
    return redirect("patientapp:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)

    appointment.status = "Completed"
    appointment.save()

    messages.success(request, "Appointment Completed Successfully")
    return redirect("patientapp:appointment_detail", appointment.appointment_id)


@login_required
def notifications(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)

    context = {
        "notifications": notifications
    }

    return render(request, "patientapp/notifications.html", context)

@login_required
def mark_noti_seen(request, id):
    patient = patient_models.Patient.objects.get(user=request.user)
    notification = patient_models.Notification.objects.get(patient=patient, id=id)
    notification.seen = True
    notification.save()
    
    messages.success(request, "Notification marked as seen")
    return redirect("patientapp:notifications")


@login_required
def profile(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    formatted_dob = patient.dob.strftime('%Y-%m-%d')
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("dob")
        blood_group = request.POST.get("blood_group")

        patient.full_name = full_name
        patient.mobile = mobile
        patient.address = address
        patient.gender = gender
        patient.date_of_birth = date_of_birth
        patient.blood_group = blood_group

        if image != None:
            patient.image = image

        patient.save()
        messages.success(request, "Profile updated successfully")
        return redirect("patientapp:profile")

    context = {
        "patient": patient,
        "formatted_dob": formatted_dob,
    }

    return render(request, "patientapp/profile.html", context)
