# Generated by Django 2.0.4 on 2018-04-23 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EREAccounts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('DocumentTrackingNumber', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('OriginalDocumentID', models.CharField(max_length=40, blank=True, null=True)),
                ('MarketerDUNS', models.CharField(blank=True, max_length=50, null=True)),
                ('UtilityDUNS', models.CharField(max_length=50, blank=True, null=True)),
                ('PaymentDueDate', models.DateField(blank=True, null=True)),
                ('ESIID', models.CharField(blank=True, max_length=40, null=True)),
                ('InvoiceTotalAmount', models.FloatField(blank=True, null=True)),
                ('Processed',models.NullBooleanField()),
                ('updatedatatime', models.DateTimeField(blank=True, null=True)),
                ('updateuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'ERE Accounts',
                'db_table': 'EREAccounts',
            },
        ),
    ]