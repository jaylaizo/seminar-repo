# Generated by Django 5.1.1 on 2025-06-04 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_instructor_check_number_seminar_eligible_programs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seminarregistration',
            name='registration_date',
        ),
        migrations.AlterField(
            model_name='seminar',
            name='time',
            field=models.CharField(max_length=20),
        ),
    ]
