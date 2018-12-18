# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Interfaces(models.Model):
    mac = models.CharField(db_column='MAC', primary_key=True, max_length=30)  # Field name made lowercase.
    matb = models.ForeignKey('Thietbi', models.DO_NOTHING, db_column='MaTB', blank=True, null=True)  # Field name made lowercase.
    tenif = models.CharField(db_column='TenIF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idx = models.IntegerField(blank=True, null=True)
    ipaddv4 = models.CharField(max_length=30, blank=True, null=True)
    inbound = models.FloatField(blank=True, null=True)
    outbound = models.FloatField(blank=True, null=True)
    trangthai = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'interfaces'


class Phongban(models.Model):
    mapb = models.CharField(db_column='MaPB', primary_key=True, max_length=30)  # Field name made lowercase.
    tenpb = models.CharField(db_column='TenPB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    network = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'phongban'


class Thietbi(models.Model):
    matb = models.CharField(db_column='MaTB', primary_key=True, max_length=30)  # Field name made lowercase.
    mapb = models.ForeignKey(Phongban, models.DO_NOTHING, db_column='MaPB', blank=True, null=True)  # Field name made lowercase.
    tentb = models.TextField(db_column='TenTB', blank=True, null=True)  # Field name made lowercase.
    socong = models.IntegerField(blank=True, null=True)
    trangthai = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'thietbi'
