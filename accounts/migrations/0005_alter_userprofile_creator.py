# Generated by Django 3.2.5 on 2021-08-19 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_leader_id_userprofile_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='creator',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.userprofile'),
        ),
    ]
