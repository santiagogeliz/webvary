# Generated by Django 3.1.5 on 2021-02-12 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datospaginas', '0003_auto_20210204_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='sitio_web',
            field=models.URLField(blank=True, help_text='Escribe la URL de un sitio web.'),
        ),
    ]