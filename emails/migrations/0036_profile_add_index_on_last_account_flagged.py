# Generated by Django 2.2.24 on 2021-12-16 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0035_profile_date_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_account_flagged',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
