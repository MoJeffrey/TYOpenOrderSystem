# Generated by Django 3.1.3 on 2020-11-18 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=128)),
                ('Label', models.CharField(max_length=248)),
                ('QuantityPerBox', models.CharField(max_length=248)),
                ('PurchasePrice', models.CharField(max_length=248)),
            ],
            options={
                'db_table': 'Product',
                'ordering': ['Name'],
                'unique_together': {('Name', 'Label')},
                'index_together': {('Name', 'Label')},
            },
        ),
    ]
