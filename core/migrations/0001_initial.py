# Generated by Django 3.2.5 on 2021-08-03 02:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20210720_0014'),
        ('career', '0002_auto_20210729_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdiMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrer_tier_goal', models.SmallIntegerField()),
                ('interest_one', models.CharField(help_text='Insira um tema de interesse', max_length=120, null=True)),
                ('interest_two', models.CharField(help_text='Insira um tema de interesse', max_length=120, null=True)),
                ('interest_three', models.CharField(help_text='Insira um tema de interesse', max_length=120, null=True)),
                ('interest_four', models.CharField(help_text='Insira um tema de interesse', max_length=120, null=True)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('carrer_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occupation_goal', to='career.occupation')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdi_follower_profile', to='accounts.userprofile')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdi_leader_profile', to='accounts.userprofile')),
            ],
            options={
                'verbose_name': 'Reunião 1:1',
                'verbose_name_plural': 'Reuniões 1:1',
            },
        ),
        migrations.CreateModel(
            name='PdiPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Descrição / Objetivo do Plano', max_length=120)),
                ('plan_type', models.SmallIntegerField(choices=[(1, 'Desenvolver'), (2, 'Aprimorar'), (3, 'Reduzir')])),
                ('pdi_meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pdimeeting')),
            ],
        ),
        migrations.CreateModel(
            name='OneOnOneMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_one', models.CharField(help_text='Insira um tópico da reunião', max_length=255)),
                ('subject_two', models.CharField(help_text='Insira um tópico da reunião', max_length=255)),
                ('subject_three', models.CharField(help_text='Insira um tópico da reunião', max_length=255)),
                ('subject_four', models.CharField(help_text='Insira um tópico da reunião', max_length=255)),
                ('subject_five', models.CharField(help_text='Insira um tópico da reunião', max_length=255)),
                ('next_meeting_date', models.DateField(default=datetime.date.today)),
                ('meetings_frequency', models.SmallIntegerField(choices=[(1, 'Semanal'), (2, 'Mensal'), (3, 'Trimestral'), (4, 'Quinzenal'), (5, 'Sem repetição')], default=1)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one_follower_profile', to='accounts.userprofile')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one_leader_profile', to='accounts.userprofile')),
            ],
            options={
                'verbose_name': 'Reunião 1:1',
                'verbose_name_plural': 'Reuniões 1:1',
            },
        ),
        migrations.CreateModel(
            name='ActionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Descreva o plano de ação', max_length='255')),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('status', models.SmallIntegerField(choices=[(1, 'Em Aberto'), (2, 'Iniciado'), (3, 'Parcial'), (4, 'Completo')])),
                ('pdi_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pdiplan')),
            ],
        ),
    ]
