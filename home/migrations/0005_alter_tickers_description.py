# Generated by Django 4.1.5 on 2023-10-13 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_bse_code_tickers_bsecode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickers',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
    ]