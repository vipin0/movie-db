# Generated by Django 3.2.5 on 2021-07-28 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieDbApp', '0009_auto_20210728_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='star',
            name='about',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='About'),
        ),
    ]