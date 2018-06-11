from django.db import models
#from reportlab.lib.colors import black

from django.db.models import F, Count, Value
from django.db.models.functions import Length, Upper

# Create your models here.

from coredrca.validators import *

class Medico(models.Model):
    nome = models.CharField(validators=[validate_domainonly_nome],max_length=30, primary_key=True)
    morada = models.CharField(max_length=150)
    telefone = models.CharField(max_length=15)
    especialidade = models.CharField(max_length=130)

    def __str__(self):
        return self.nome

class Utente(models.Model):
    nome = models.CharField(max_length=30, primary_key=True)
    morada = models.CharField(max_length=150)
    telefone = models.CharField(max_length=15)
    idMedico = models.ManyToManyField(Medico)


    def __str__(self):
        return self.nome

class Infarmed(models.Model):
    nome = models.CharField(max_length=30, primary_key=True)
    def __str__(self):
        return self.nome

class Receita(models.Model):
    nome = models.CharField(max_length=30, primary_key=True)
    idMedico = models.ForeignKey(Medico, Medico)
    idUtente = models.ForeignKey(Utente, Utente)

    def __str__(self):
        return self.nome


class MedReceita(models.Model):
    nome= models.ForeignKey(Infarmed, Infarmed)
    quant = models.PositiveIntegerField()
    idReceita = models.ForeignKey(Receita, Receita)


class Farmacia(models.Model):
    nome = models.CharField(max_length=30, primary_key=True)
    #idReceita=models.ManyToManyField(Receita)
    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    nome = models.ForeignKey(Infarmed, Infarmed)
    quantidade = models.PositiveIntegerField()
    idFarmacia=models.ForeignKey(Farmacia, Farmacia)


class Aviar(models.Model):
    idFarmacia = models.ForeignKey(Farmacia, Farmacia)
    idReceita=models.ForeignKey(Receita, Receita)