# Generated by Django 5.0.6 on 2024-06-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay_info',
            name='location',
            field=models.TextField(max_length=100),
        ),
    ]
