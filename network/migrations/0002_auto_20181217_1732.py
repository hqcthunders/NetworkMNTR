# Generated by Django 2.1.4 on 2018-12-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interfaces',
            name='tenif',
            field=models.CharField(blank=True, db_column='TenIF', max_length=255, null=True),
        ),
    ]