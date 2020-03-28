# Generated by Django 3.0.3 on 2020-03-24 02:33

from django.db import migrations, models
import listing.models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='dimensions',
        ),
        migrations.AddField(
            model_name='listing',
            name='dimensions1',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='dimensions2',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='unit',
            field=models.CharField(default='cm', max_length=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to=listing.models.get_upload_path),
        ),
    ]
