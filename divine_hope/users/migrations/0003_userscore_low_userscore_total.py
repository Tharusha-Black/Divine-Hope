# Generated by Django 4.2.3 on 2023-09-20 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_userscore_aptest_alter_userscore_engtest_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userscore",
            name="low",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userscore",
            name="total",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]