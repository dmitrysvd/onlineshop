# Generated by Django 3.1.1 on 2020-11-21 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='second_name',
            new_name='last_name',
        ),
    ]