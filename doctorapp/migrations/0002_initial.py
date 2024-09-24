# Generated by Django 4.2.2 on 2024-09-24 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctorapp', '0001_initial'),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointment_notification', to='mainapp.appointment'),
        ),
        migrations.AddField(
            model_name='notification',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctorapp.doctor'),
        ),
    ]
