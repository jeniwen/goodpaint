# Generated by Django 3.0.4 on 2020-04-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0005_auto_20200324_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='descrip',
            field=models.CharField(blank=True, max_length=10000),
        ),
    ]
