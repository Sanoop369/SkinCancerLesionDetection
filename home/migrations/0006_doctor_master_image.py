# Generated by Django 4.2.2 on 2023-10-02 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_patient_report_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor_master',
            name='image',
            field=models.ImageField(null=True, upload_to='doctor'),
        ),
    ]
