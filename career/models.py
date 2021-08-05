from django.db import models
from django.db.models.base import Model

# Create your models here.

class Skill(models.Model):
    name = models.TextField('Nome', max_length = 200)
    description = models.TextField('Descrição', null=True)

    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.TextField('Cargo', max_length = 200)
    level = models.SmallIntegerField()
    tier = models.SmallIntegerField()
    description = models.TextField('Descrição', null=True)
    skills = models.ManyToManyField(Skill, related_name='skill')

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.name
    
    