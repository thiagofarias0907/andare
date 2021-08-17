# Generated by Django 3.2.5 on 2021-08-16 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0002_auto_20210729_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occupation',
            name='skills',
        ),
        migrations.AddField(
            model_name='skill',
            name='occupation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='career.occupation'),
            preserve_default=False,
        ),
    ]