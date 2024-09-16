# Generated by Django 5.1.1 on 2024-09-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='Ozel_istek',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('Deluxe', 'Deluxe Bahceli Oda'), ('Standard', 'Standart Oda'), ('Suite', 'Suite Oda'), ('Deluxe cift', 'Deluxe Bahceli Cift Kisilik Oda'), ('Standard cift ', 'Standart Cift Kisilik Oda')], max_length=50),
        ),
    ]
