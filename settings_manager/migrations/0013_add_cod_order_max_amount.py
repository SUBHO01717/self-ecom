from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_manager', '0012_alter_sitesettings_font_family'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='cod_order_max_amount',
            field=models.DecimalField(
                default='0.00',
                help_text="Maximum order total allowed for Cash on Delivery. Set to 0 to allow COD for all orders.",
                max_digits=10,
                decimal_places=2,
            ),
        ),
    ]
