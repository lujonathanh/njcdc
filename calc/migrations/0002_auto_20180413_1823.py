# Generated by Django 2.0.3 on 2018-04-13 18:23

import calc.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gasoline_amt',
            field=models.FloatField(default=200.0, validators=[calc.models.validate_nonnegative]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='period',
            field=models.CharField(choices=[('month', 'Per Month')], default='month', help_text='Time range for calculation.', max_length=5),
        ),
    ]
