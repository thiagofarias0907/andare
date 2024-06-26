# Generated by Django 3.2.5 on 2021-07-30 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200, verbose_name='Nome')),
                ('description', models.TextField(null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Habilidade',
                'verbose_name_plural': 'Habilidades',
            },
        ),
        migrations.AddField(
            model_name='occupation',
            name='skills',
            field=models.ManyToManyField(related_name='skill', to='career.Skill'),
        ),
    ]
