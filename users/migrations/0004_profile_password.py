# Generated by Django 3.2.8 on 2021-11-29 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_content_description_bill_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
