# Generated by Django 4.0.6 on 2022-07-20 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_alter_item_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='modified_at',
            field=models.DateTimeField(null=True, verbose_name='date modified'),
        ),
    ]