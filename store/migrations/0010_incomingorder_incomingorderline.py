# Generated by Django 3.2.10 on 2022-02-05 11:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_product_count_sold'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='سعر الفاتوره')),
                ('remaining_money', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='رصيد ما قبله')),
                ('total2', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='الاجمالى')),
                ('paid', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='تم دفع')),
                ('still', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='مازال')),
                ('ORDslug', models.SlugField(allow_unicode=True, blank=True, max_length=255, null=True, unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='IncomingOrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='الكميه')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('incomingorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.incomingorder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='المنتج')),
            ],
            options={
                'ordering': ['product'],
            },
        ),
    ]