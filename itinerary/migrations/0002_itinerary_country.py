# Generated by Django 4.0.4 on 2023-07-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='country',
            field=models.CharField(blank=True, choices=[(None, 'Select Country'), ('Italy', 'Italy'), ('Romania', 'Romania'), ('Switzerland', 'Switzerland'), ('Germany', 'Germany'), ('France', 'France'), ('Spain', 'Spain'), ('Portugal', 'Portugal'), ('Belgium', 'Belgium'), ('Austria', 'Austria'), ('Slovenia', 'Slovenia'), ('Hungary', 'Hungary'), ('Croatia', 'Croatia'), ('Bulgaria', 'Bulgaria'), ('Czech Republic', 'Czech Republic'), ('Poland', 'Poland'), ('Sweden', 'Sweden'), ('Norway', 'Norway'), ('Denmark', 'Denmark')], max_length=50, verbose_name='Country'),
        ),
    ]