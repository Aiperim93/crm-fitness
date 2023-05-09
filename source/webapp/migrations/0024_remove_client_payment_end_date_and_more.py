# Generated by Django 4.1.7 on 2023-04-19 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_remove_coach_telegram_name_coach_telegram_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='payment_end_date',
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания оплаты'),
        ),
    ]
