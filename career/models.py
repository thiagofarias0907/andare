from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

# Create your models here.

class Occupation(models.Model):
    name = models.CharField('Cargo', max_length = 100)
    level = models.SmallIntegerField('Nível')
    tier = models.SmallIntegerField('Subnível')
    description = models.CharField('Descrição', null=True, max_length = 200)
    # skills = models.ManyToManyField(Skill, related_name='skill')

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField('Habilidade', max_length = 100)
    description = models.CharField('Descrição', null=True, max_length = 200)
    occupation = models.ForeignKey(Occupation,on_delete=CASCADE)

    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.name

    