# Generated by Django 3.2.5 on 2021-08-18 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0003_auto_20210816_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='description',
            field=models.CharField(max_length=200, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='level',
            field=models.SmallIntegerField(verbose_name='Nível'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Cargo'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='tier',
            field=models.SmallIntegerField(verbose_name='Subnível'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.CharField(max_length=200, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Habilidade'),
        ),
    ]
