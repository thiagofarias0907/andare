from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import User
from career.models import Occupation 

# Create your models here.


class UserProfile(models.Model):
    PROFILE_CHOICES = [(1,'Colaborador'),(2,'Líder')]

    picture = models.ImageField('Foto', upload_to='user_profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile = models.SmallIntegerField(choices=PROFILE_CHOICES, default=1)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name= 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
        
    def __str__(self):
        return "{} {} - {}".format(self.user.first_name, self.user.last_name, self.occupation.name)

    # def clean(self):
    #     model = self.__class__
    #     if model.objects.count() > 0 and self.id != model.objects.get().id:
    #         raise ValidationError("Já existe um perfil cadastrado para este usuário!")