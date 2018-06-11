# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import RequestContext, loader
from coredrca.models import *
from coredrca.admin import *
from datetime import datetime
from django.template import Context, Template
from django.shortcuts import redirect
from django.contrib import admin
from coredrca.forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Avg, Sum, Count, Max, Min
from django.views.generic import TemplateView
from django.contrib.messages import constants as messages

# Create your views here.

def home(request):
    template = loader.get_template('index.html')
    context = {'re':request}
    return HttpResponse(template.render(context))


#--------------- Médicos --------------------

def medicos(request):
    medicos = Medico.objects.all()
    #teste = 'Alunos'
    template = loader.get_template('medicos.html')
    context = {'medicos':medicos}
    return HttpResponse(template.render(context))

#Adicionar Médico:

def getMedico(request):
    if request.method=='POST':
        form=PostForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('medico')
        else:
            messages.error(request, 'Error')
    form=PostForm()
    return render(request, 'cadastro-medicos.html', {'form':form})

#Informações do Médico:
def medico_detail(request, nome):
    medico=Medico.objects.get(nome=nome)
    receita=Receita.objects.filter(idMedico=nome).values('nome')
    #medreceita=MedReceita.objects.filter(idReceita=receita)
    #medreceita=medrec[0]


    numRecMed = Receita.objects.values('idMedico').filter(idMedico=nome).annotate(num=Count('idMedico'))
    numRmedi=numRecMed.values_list('num')


    num_entries = Receita.objects.filter(idMedico=nome).count()
    num_receit = Receita.objects.aggregate(num_rec=Count('nome', distinct=True))
    media= (num_entries / float(num_receit['num_rec']))*100


    return render(request, 'info-medico.html', {'medico': medico, 'receita':receita, 'numRmedi':numRmedi, 'media':media })


#--------------- Utentes -------------

def utentes(request):
    utentes = Utente.objects.all()
    template = loader.get_template('utentes.html')
    context = {'utentes':utentes}
    return HttpResponse(template.render(context))


def getUtente(request):
    if request.method=='POST':
        form=PostForm2(request.POST)

        if form.is_valid():
            form.save()
            return redirect('utente')
        else:
            messages.error(request, 'Error')
    form=PostForm2()
    return render(request, 'cadastro-utentes.html', {'form':form})

def utente_detail(request, nome):
    utente=Utente.objects.get(nome=nome)
    receita=Receita.objects.filter(idUtente=nome)

    numRecUte = Receita.objects.values('idUtente').filter(idUtente=nome).annotate(num=Count('idUtente'))
    numRuten=numRecUte.values_list('num')

    num_entries = Receita.objects.filter(idUtente=nome).count()
    num_receit = Receita.objects.aggregate(num_rec=Count('nome', distinct=True))
    media= (num_entries / float(num_receit['num_rec']))*100


    return render(request, 'info-utente.html', {'utente': utente, 'receita':receita, 'numRuten':numRuten, 'media':media})


#----------------------- Receitas -----------------

def receitas(request):
    template = loader.get_template('receitas.html')
    receitas = Receita.objects.all()



#Número de Receitas:
    numR = Receita.objects.aggregate(numR=Count('nome', distinct=True))
    numRec = numR.values()

#número de Utentes com Receitas:
    numU=Receita.objects.aggregate(num=Count('idUtente', distinct=True))
    numUte = (numU).values()


# Média de Receitas por Utente:
    MedRU = float(numR['numR'])/float(numU['num'])


#Utente com mais receitas:
    numReU=Receita.objects.values('idUtente').annotate(count=Count("idUtente"))
    nReUte=numReU.order_by('-count')
    numReUt=list(nReUte)
    numReUte=numReUt[0:3]

# Utente com menos receitas:

    nReUteMenos = numReU.order_by('count')
    numReUt = list(nReUteMenos)
    numReUteMe = numReUt[0:3]

# Médico com mais receitas:
    numReMedi = Receita.objects.values('idMedico').annotate(count=Count("idMedico"))
    nReMe = numReMedi.order_by('-count')
    numReM = list(nReMe)
    numReMedico = numReM[0:3]

# Médico com menos receitas:

    nReMeMenos = numReMedi.order_by('count')
    numReMen = list(nReMeMenos)
    numReMedicMenos = numReMen[0:3]


# Medicamento com mais quantidade nas receitas:
    numReMedicamen = MedReceita.objects.values('nome').annotate(count=Sum("quant"))
    numReMedica = numReMedicamen.order_by('-count')
    numReMedicam = list(numReMedica)
    numReMedicamento = numReMedicam[0:3]

# Medicamento com menos quantidade receitas:

    nReMediMenos = numReMedicamen.order_by('count')
    numReMenMedi = list(nReMediMenos)
    numReMedicaMenos = numReMenMedi[0:3]


# número de Médicos com Receitas:
    numM = Receita.objects.aggregate(num=Count('idMedico', distinct=True))


# Média de Receitas por Médico:
    MedRM = float(numR['numR']) / float(numM['num'])

    context = {'receitas':receitas, 'numRec':numRec, 'numUte':numUte, 'MedRU':MedRU, 'numReUte':numReUte, 'numReUteMe':numReUteMe, 'numReMedico':numReMedico, 'numReMedicMenos':numReMedicMenos, 'numReMedicamento':numReMedicamento, 'numReMedicaMenos':numReMedicaMenos, 'MedRM':MedRM}

    return HttpResponse(template.render(context))


#-------------Adicionar Receita:-----------
#(1 Medicamento por Receita)

def getReceita(request):
    if request.method=='POST':
        form=PostForm3(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receita')
        else:
            messages.error(request, 'Error')
    form=PostForm3()
    return render(request, 'cadastro-receitas.html', {'form':form})


def receita_detail(request, nome):
    receita = Receita.objects.filter(nome=nome)
    medicamento=MedReceita.objects.filter(idReceita=nome)
    return render(request, 'info-receita.html', {'receita': receita, 'medicamento':medicamento })



#-------------- Medicamentos no Stock da Farmácia -----------------------

def medicamentos(request):
    medicamentos = Medicamento.objects.all()

    #farmacias=Farmacia.objects.all()
    template = loader.get_template('medicamentos.html')
    context = {'medicamentos':medicamentos}
    return HttpResponse(template.render(context))

def getMedicamento(request):
    if request.method=='POST':
        form=PostForm4(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicamento')
        else:
            messages.error(request, 'Error')
    form=PostForm4()
    return render(request, 'cadastro-medicamentos.html', {'form':form})

#--------------------- Farmácias ----------------------
def farmacias(request):
    farmacias = Farmacia.objects.all()
    template = loader.get_template('farmacias.html')
    context = {'farmacias':farmacias}
    return HttpResponse(template.render(context))

def getFarmacia(request):
    if request.method=='POST':
        form=PostForm5(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmacias')
        else:
            messages.error(request, 'Error')
    form=PostForm5()
    return render(request, 'cadastro-farmacias.html', {'form':form})


#---------------- Aviar -----------------

def aviar(request):
    aviar = Aviar.objects.all()
    receita=Receita.objects.all()
    template = loader.get_template('aviar.html')
    context = {'aviar':aviar, 'receita':receita}
    return HttpResponse(template.render(context))

#Apagar a Receita do Aviar e apagar das Receitas- "Aviar a Receita"
def deletereceita(request, pk):
    a = Aviar.objects.filter(pk=pk).values_list('idReceita')
    nome=(list(a[0])[0])
    medrec=MedReceita.objects.filter(idReceita=nome).values_list('nome')
    medic=(list(medrec[0])[0])
    aviar = Aviar.objects.filter(pk=pk)
    medicamento=MedReceita.objects.filter(nome=medic)
    recei = Receita.objects.filter(nome=nome)
    aviar and aviar[0].delete()
    medicamento and medicamento[0].delete()
    recei and recei[0].delete()
    return HttpResponseRedirect(reverse('aviar'))

#---------------Medicamento da Receita---------------

def getMedicReceita(request):
    if request.method=='POST':
        form=PostForm6(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmacias')
        else:
            messages.error(request, 'Error')
    form=PostForm6()
    return render(request, 'cadastro-rec.html', {'form':form})


#-----------------Repor Stock -----------------

def getMedicStock(request):

    if request.method=='POST':
        form=PostForm7(request.POST)
        if form.is_valid():
            #form.save()
            return redirect('medicamento')

    form=PostForm7()
    return render(request, 'addStock.html', {'form':form})



#---------------Inserir Receita Farmácia -----------------
#(Sem os Medicamentos e quantidade. Apenas o médico e o utente.)

def getRecFarm(request):
    if request.method=='POST':
        form=PostForm8(request.POST)

        if form.is_valid():
            form.save()
            return redirect('receita')

    form=PostForm8()
    return render(request, 'addRec.html', {'form':form})


#----------------- Infarmed ------------
#Todos os medicamentos válidos
def infarmed(request):
    infarmed = Infarmed.objects.all()
    template = loader.get_template('infarmed.html')
    context = {'infarmed':infarmed}
    return HttpResponse(template.render(context))


def getInfarmed(request):
    if request.method=='POST':
        form=PostForm9(request.POST)

        if form.is_valid():
            form.save()
            return redirect('infarmed')
        else:
            messages.error(request, 'Error')
    form=PostForm9()
    return render(request, 'cadastro-infarmed.html', {'form':form})

