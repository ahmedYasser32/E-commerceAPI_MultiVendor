# Generated by Django 4.0.6 on 2022-07-20 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_alter_item_modified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
