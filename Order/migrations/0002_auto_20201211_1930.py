# Generated by Django 3.1.3 on 2020-12-11 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='OrderID',
            field=models.IntegerField(db_index=True),
        ),
    ]