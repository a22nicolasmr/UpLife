# Generated by Django 4.2.20 on 2025-05-05 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UpLife_api', '0012_alter_plantillas_icona'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantillas',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='UpLife_api.usuarios'),
        ),
    ]
