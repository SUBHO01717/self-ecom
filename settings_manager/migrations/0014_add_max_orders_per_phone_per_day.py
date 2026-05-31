from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_manager', '0013_add_cod_order_max_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='max_orders_per_phone_per_day',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Maximum number of orders allowed per phone number in 24 hours. Set 0 to allow unlimited orders.',
            ),
        ),
    ]
