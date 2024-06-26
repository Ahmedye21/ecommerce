# Generated by Django 5.0.6 on 2024-06-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('name',), 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='items_images/'),
        ),
    ]
