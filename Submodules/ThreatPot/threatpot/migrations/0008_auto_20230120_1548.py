# Generated by Django 3.2.16 on 2023-01-20 15:48

from django.db import migrations


def generalHoneypot(apps, schema_editor):
    GeneralHoneypot = apps.get_model("threatpot", "GeneralHoneypot")
    general_honeypots = [
        "Heralding",
        "Ciscoasa",
        "Honeytrap",
        "Dionaea",
        "ConPot",
        "Adbhoney",
        "Tanner",
        "CitrixHoneypot",
        "Mailoney",
        "Ipphoney",
        "Ddospot",
        "ElasticPot",
        "Dicompot",
        "Redishoneypot",
        "Sentrypeer",
        "Glutton",
    ]
    for hp in general_honeypots:
        honeypot = GeneralHoneypot(name=hp)
        honeypot.save()


class Migration(migrations.Migration):

    dependencies = [
        ("threatpot", "0007_generalhoneypot"),
    ]

    operations = [migrations.RunPython(generalHoneypot)]
