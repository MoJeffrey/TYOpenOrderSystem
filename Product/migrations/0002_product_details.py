# Generated by Django 3.1.3 on 2021-02-04 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Details',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]