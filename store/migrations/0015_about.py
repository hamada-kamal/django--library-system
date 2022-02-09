# Generated by Django 3.2.10 on 2022-02-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20220207_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56, unique=True, verbose_name='الاسم')),
                ('phone1', models.CharField(blank=True, max_length=11, null=True, verbose_name='رقم الهاتف 1')),
                ('phone2', models.CharField(blank=True, max_length=11, null=True, verbose_name='رقم الهاتف 2')),
            ],
        ),
    ]
