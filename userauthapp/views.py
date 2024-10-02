from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauthapp import forms as userauths_forms
from userauthapp import models as userauths_models
from doctorapp import models as doctor_models
from patientapp import models as patient_models

def register_view(request):
    if request.user.is_authenticated:       #if user already logged in then redirect to home page
        messages.success(request, "You are already logged in!!")
        return redirect("/")
    
    if request.method == "POST":        #getting the information from the form directly
        form = userauths_forms.UserRegisterForm(request.POST or None)       #request.POST will grab whatever that was sent in the POST and it will save it in the form variable and save the new user to the database

        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")

            user = authenticate(request, email=email, password=password1)       #immediate login after registration
            print("user ========= ", user)

            if user is not None:
                login(request, user)

                if user_type == "Doctor":
                    doctor_models.Doctor.objects.create(user=user, full_name=full_name)
                else:
                    patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)

                messages.success(request, "Account created successfully")
                return redirect("/")        #redirect user to home page

            else:
                messages.error(request, "Authenticated failed, please try again!")

    else:
        form = userauths_forms.UserRegisterForm()

    context = {
        "form":form
    }
    return render(request, "userauthapp/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    if request.method == "POST":        #request.POST will grab whatever that was sent in the POST and it will save it in the form variable
        form = userauths_forms.LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user_instance = userauths_models.User.objects.get(email=email, is_active=True)      #is_active is used to filter only active user that is not banned
                user_authenticate = authenticate(request, email=email, password=password)

                if user_instance is not None:
                    login(request, user_authenticate)

                    messages.success(request, "Account created successfully")
                    
                    next_url = request.GET.get("next", '/')
                    return redirect(next_url)
                else:
                    messages.error(request, "User Name Or Password Does Not Exist!")
            except:
                messages.error(request, "User does not exist!")
    else:
        form = userauths_forms.LoginForm()  #
    
    context = {
        "form":form
    }
    return render(request, "userauthapp/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect("userauthapp:sign-in")