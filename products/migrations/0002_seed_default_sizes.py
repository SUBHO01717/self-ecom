from django.db import migrations


def seed_sizes(apps, schema_editor):
    Size = apps.get_model("products", "Size")
    for order, name in enumerate(["One Size", "Small", "Medium", "Large", "Extra Large", "Double Extra Large"]):
        Size.objects.get_or_create(name=name, defaults={"display_order": order})


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_sizes, migrations.RunPython.noop),
    ]
