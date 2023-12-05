# Generated by Django 4.2.6 on 2023-12-02 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactions',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='billing.customer'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bundle',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bundle_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bundle',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bundle_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='customer',
            constraint=models.UniqueConstraint(fields=('telephone_one',), name='customer_unique'),
        ),
        migrations.AddConstraint(
            model_name='customer',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name'), name='firstname_last_name'),
        ),
        migrations.AddConstraint(
            model_name='bundle',
            constraint=models.UniqueConstraint(fields=('bundle_data', 'bundle_duration', 'bundle_limitted'), name='data_duration_limitted'),
        ),
    ]