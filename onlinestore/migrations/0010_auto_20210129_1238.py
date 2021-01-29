# Generated by Django 3.1.4 on 2021-01-29 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0009_auto_20201226_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='engine_power',
        ),
        migrations.RemoveField(
            model_name='product',
            name='engine_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='manufacturer_country',
        ),
        migrations.RemoveField(
            model_name='product',
            name='model_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='number_of_seats',
        ),
        migrations.RemoveField(
            model_name='product',
            name='year_of_issue',
        ),
        migrations.CreateModel(
            name='ProductAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer_country', models.CharField(choices=[('canada', 'Канада'), ('usa', 'Америка'), ('russia', 'Россия'), ('china', 'Китай')], max_length=10)),
                ('model_name', models.CharField(max_length=200)),
                ('engine_power', models.IntegerField()),
                ('engine_type', models.CharField(choices=[('gas', 'Бензиновый'), ('electric', 'Электрический'), ('diesel', 'Дизельный')], max_length=10)),
                ('number_of_seats', models.IntegerField()),
                ('year_of_issue', models.IntegerField()),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='onlinestore.brand')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='onlinestore.product')),
            ],
        ),
    ]
