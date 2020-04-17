# Generated by Django 3.0.4 on 2020-04-16 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0005_auto_20200324_1829'),
        ('shopping_cart', '0004_auto_20200416_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='listing.Listing'),
            preserve_default=False,
        ),
    ]
