# Generated by Django 2.1.4 on 2018-12-17 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interfaces',
            fields=[
                ('mac', models.CharField(db_column='MAC', max_length=30, primary_key=True, serialize=False)),
                ('tenif', models.CharField(blank=True, db_column='TenIF', max_length=30, null=True)),
                ('idx', models.IntegerField(blank=True, null=True)),
                ('ipaddv4', models.CharField(blank=True, max_length=30, null=True)),
                ('inbound', models.FloatField(blank=True, null=True)),
                ('outbound', models.FloatField(blank=True, null=True)),
                ('trangthai', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'interfaces',
            },
        ),
        migrations.CreateModel(
            name='Phongban',
            fields=[
                ('mapb', models.CharField(db_column='MaPB', max_length=30, primary_key=True, serialize=False)),
                ('tenpb', models.CharField(blank=True, db_column='TenPB', max_length=30, null=True)),
                ('network', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'phongban',
            },
        ),
        migrations.CreateModel(
            name='Thietbi',
            fields=[
                ('matb', models.CharField(db_column='MaTB', max_length=30, primary_key=True, serialize=False)),
                ('tentb', models.TextField(blank=True, db_column='TenTB', null=True)),
                ('socong', models.IntegerField(blank=True, null=True)),
                ('trangthai', models.IntegerField(blank=True, null=True)),
                ('mapb', models.ForeignKey(blank=True, db_column='MaPB', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='network.Phongban')),
            ],
            options={
                'db_table': 'thietbi',
            },
        ),
        migrations.AddField(
            model_name='interfaces',
            name='matb',
            field=models.ForeignKey(blank=True, db_column='MaTB', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='network.Thietbi'),
        ),
    ]