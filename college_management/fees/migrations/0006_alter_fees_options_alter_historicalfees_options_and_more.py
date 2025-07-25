# Generated by Django 5.2.4 on 2025-07-03 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0005_student_mother_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fees',
            options={'verbose_name': 'Fees', 'verbose_name_plural': 'Fees'},
        ),
        migrations.AlterModelOptions(
            name='historicalfees',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Fees', 'verbose_name_plural': 'historical Fees'},
        ),
        migrations.AlterField(
            model_name='fees',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='fees.student'),
        ),
    ]
