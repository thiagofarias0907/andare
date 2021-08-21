from datetime import date, datetime, timedelta
from time import time
from accounts.models import UserProfile
from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from career.models import Occupation
# Create your models here.

class OneOnOneMeeting(models.Model):
    FREQUENCY_CHOICES = [(1,'Semanal'),(2,'Mensal'),(3,'Trimestral'),(4,'Quinzenal'), (5,'Sem repetição')]
    
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='one_follower_profile')
    leader   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='one_leader_profile')
    subject_one = models.CharField(help_text='Insira um tópico da reunião', max_length=255)
    subject_two = models.CharField(help_text='Insira um tópico da reunião', max_length=255, null=True, blank=True)
    subject_three = models.CharField(help_text='Insira um tópico da reunião', max_length=255, null=True, blank=True)
    subject_four = models.CharField(help_text='Insira um tópico da reunião', max_length=255, null=True, blank=True)
    subject_five = models.CharField(help_text='Insira um tópico da reunião', max_length=255, null=True, blank=True)
    next_meeting_date = models.DateField(default=date.today) #default=timezone.now, 
    meetings_frequency = models.SmallIntegerField(choices=FREQUENCY_CHOICES, default=1)
    date_time = models.DateTimeField(auto_now=True) #default=timezone.now 

    class Meta:
        verbose_name= 'Reunião 1:1'
        verbose_name_plural= 'Reuniões 1:1'
    
    def __str__(self):
        return self.leader.user.first_name + ':' + self.follower.user.first_name
    
class PdiMeeting(models.Model):
    CAREER_TIER_GOAL = [(1,'Nível 1'),(2,'Nível 2'),(3,'Nível 3'),(4,'Nível 4')]
    
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pdi_follower_profile')
    leader   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pdi_leader_profile')

    career_goal = models.ForeignKey(Occupation, on_delete=models.CASCADE, related_name='occupation_goal')
    career_tier_goal = models.SmallIntegerField(choices=CAREER_TIER_GOAL, default=1)

    interest_one = models.CharField(help_text='Insira um tema de interesse'  , max_length=120, null=True)
    interest_two = models.CharField(help_text='Insira um tema de interesse'  , max_length=120, null=True)
    interest_three = models.CharField(help_text='Insira um tema de interesse', max_length=120, null=True)
    interest_four = models.CharField(help_text='Insira um tema de interesse' , max_length=120, null=True)

    date_time  = models.DateTimeField(auto_now=True)  
    next_meeting = models.DateField(default=datetime.today()+timedelta(days=90))

    class Meta:
        verbose_name= 'Reunião 1:1'
        verbose_name_plural= 'Reuniões 1:1'
    
    def __str__(self):
        return self.leader.user.first_name + ':' + self.follower.user.first_name


class PdiPlan(models.Model):
    TYPE_CHOICES = [(1,'Desenvolver'),(2,'Aprimorar'),(3,'Reduzir')]

    description  = models.CharField(help_text='Descrição / Objetivo do Plano'  , max_length=120)
    plan_type    = models.SmallIntegerField(choices=TYPE_CHOICES, default=1)
    # actions_plan = models.ManyToManyField(ActionPlan) 

    pdi_meeting = models.ForeignKey(PdiMeeting, on_delete=models.CASCADE)

class ActionPlan(models.Model):
    STATUS_CHOICES = [(1,'Em Aberto'),(2,'Iniciado'),(3,'Parcial'),(4,'Completo')]
    description = models.CharField(help_text='Descreva o plano de ação', max_length=255)
    due_date    = models.DateField(default=date.today)
    status      = models.SmallIntegerField(choices=STATUS_CHOICES)
    pdi_plan    = models.ForeignKey(PdiPlan, on_delete=models.CASCADE)
    
class MeetingEvaluation(models.Model):
    EMOJI_CHOICES = [(1,'&#128557;','😭'),(2,'&#128552;','😨'),(3,'&#128560;','😰'),
                     (4,'&#128551;','😧'),(5,'&#128543;','😟'),(6,'&#128542;','😞'),
                     (7,'&#128533;','😕'),(8,'&#128524;','😌'),(9,'&#128521;','😉'),
                     (10,'&#128540;','😜'),(11,'&#128578;','🙂'),(12,'&#129322;','😊'),
                     (13,'&#128526;','😎'),(14,'&#128513;','😁'),(15,'&#129321;','🤩')
                     ]               
    feeling = models.SmallIntegerField()
    score = models.SmallIntegerField()
    commentary = models.TextField(max_length=300, null=True)
    one_on_one = models.ForeignKey(OneOnOneMeeting, on_delete=models.CASCADE, null=True, related_name='one_on_one')
    pdi_meeting = models.ForeignKey(PdiMeeting, on_delete=models.CASCADE, null=True, related_name='pdi_meeting')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    date_time = models.DateTimeField(default=datetime.now)
