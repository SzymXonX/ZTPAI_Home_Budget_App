# Generated by Django 4.2.7 on 2025-05-05 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_expense', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
