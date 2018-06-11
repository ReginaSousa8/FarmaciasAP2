from django.forms import ModelForm
from django import forms
from coredrca.models import *
from django.forms import CharField
from django.core import validators
from django import forms
from django.core.exceptions import ValidationError
from coredrca.validators import *

#inserir Médico
class PostForm(forms.ModelForm):

    nome = forms.CharField(validators=[validate_domainonly_nome], max_length=30)

    class Meta:
        model = Medico
        fields = ('nome', 'morada', 'telefone', 'especialidade')

    def clean_nome(self):
        nome_passed=self.cleaned_data.get('nome')
        nome_req ='None'
        if nome_req in nome_passed:
            raise forms.ValidationError('não válido')
        return nome_passed


    def clean(self):
        cleaned_data=super(PostForm,self).clean()
        nome_passed=cleaned_data.get('nome')
        nome_req ='None'
        if nome_req in nome_passed:
            raise forms.ValidationError('não válido')

#inserir Utente
class PostForm2(forms.ModelForm):
    nome = forms.CharField(validators=[validate_domainonly_nome], max_length=30)
    class Meta:
        model= Utente
        fields= ('nome', 'morada', 'telefone', 'idMedico')

    def clean(self):
        cleaned_data=super(PostForm2,self).clean()
        nome_passed=cleaned_data.get('nome')
        nome_req ='None'
        if nome_req in nome_passed:
            raise forms.ValidationError('não válido')

#inserir Receita
class PostForm3(forms.ModelForm):
    nome = forms.CharField(validators=[validate_domainonly_nome], max_length=30)
    class Meta:
        model= Receita
        fields= ('nome', 'idMedico', 'idUtente')

    def clean(self):
        cleaned_data=super(PostForm3,self).clean()
        nome_passed=cleaned_data.get('nome')



#Inserir Medicamento no Stock da Farmácia
class PostForm4(forms.ModelForm):

    class Meta:
        model= Medicamento
        fields= ('nome', 'quantidade', 'idFarmacia')
    def clean(self):
        cleaned_data=super(PostForm4,self).clean()
        medica = cleaned_data.get('nome')
        farmacia = cleaned_data.get('idFarmacia')
        a = Medicamento.objects.filter(idFarmacia=farmacia).filter(nome=medica).values_list('nome')

        #med = MedReceita.objects.filter(idReceita=receita).values_list('nome')
        if list(a) != []:
            medicamentos = list(a[0])[0]
            # medicamentos=MedReceita.objects.filter(idReceita=receita).values('nome')
            if medica in medicamentos:
                raise forms.ValidationError('Já foi inserido no stock da farmácia. Basta Atualizar o Stock.')



#inserir Farmácia
class PostForm5(forms.ModelForm):
    nome = forms.CharField(validators=[validate_domainonly_nome], max_length=30)
    class Meta:
        model= Farmacia
        fields= ('nome',)

    def clean(self):
        cleaned_data=super(PostForm5,self).clean()
        nome_passed=cleaned_data.get('nome')
        nome_req ='None'
        if nome_req in nome_passed:
            raise forms.ValidationError('não válido')


#inserir Medicamento Receita

class PostForm6(forms.ModelForm):
    class Meta:
        model = MedReceita
        fields = ('nome', 'quant', 'idReceita')

    def clean(self):
        cleaned_data = super(PostForm6, self).clean()
        medica = cleaned_data.get('nome')
        receita = cleaned_data.get('idReceita')
        a=MedReceita.objects.filter(idReceita=receita).values('nome')

        med = MedReceita.objects.filter(idReceita=receita).values_list('nome')
        if list(med) !=[]:
            medicamentos = list(a[0])[0]
            #medicamentos=MedReceita.objects.filter(idReceita=receita).values('nome')
            if medica in medicamentos:
                raise forms.ValidationError('não válido')

#Repor Stock
class PostForm7(forms.ModelForm):
    idFarmacia=forms.ModelChoiceField(queryset=Farmacia.objects.all())
    class Meta:
        model = Medicamento
        fields = ('nome', 'quantidade', 'idFarmacia')

    def clean(self):
        cleaned_data = super(PostForm7, self).clean()
        med=Medicamento.objects.filter(idFarmacia=self.cleaned_data.get('idFarmacia')).filter(nome=self.cleaned_data.get('nome'))

        disp = Medicamento.objects.filter(idFarmacia=self.cleaned_data.get('idFarmacia')).filter(nome=self.cleaned_data.get('nome')).values_list('quantidade')

        if list(med)==[]:
            raise ValidationError('Não há esse medicamento no stock')

        else:
            dispo=int(list(disp[0])[0])
            dis=dispo+int(self.cleaned_data['quantidade'])
            Medicamento.objects.filter(idFarmacia=self.cleaned_data.get('idFarmacia')).filter(nome=self.cleaned_data.get('nome')).update(**{'quantidade':dis})


#Adicionar Receita na farmácia (só se a farmácia tiver esse medicamento em stock)
class PostForm8(forms.ModelForm):
    class Meta:
        model = Aviar
        fields = ('idReceita', 'idFarmacia')

    def clean(self):
        cleaned_data = super(PostForm8, self).clean()
        receita = cleaned_data.get('idReceita')
        farmacia=cleaned_data.get('idFarmacia')

        #nome do medicamento:
        med=MedReceita.objects.filter(idReceita=receita).values_list('nome')
        medicamento=list(med[0])[0]

        quantRec=MedReceita.objects.filter(idReceita=receita).values('nome').values_list('quant')
        qReceita=int(list(quantRec[0])[0])

        medSto=Medicamento.objects.values('idFarmacia').filter(idFarmacia=farmacia).values_list('nome').filter(nome=medicamento).values_list('quantidade')

        medicamen=Medicamento.objects.values('idFarmacia').filter(idFarmacia=farmacia).values_list('nome').filter(nome=medicamento)
        #lm=list(medicamen[0])

        a = Aviar.objects.filter(idReceita=receita).filter(idFarmacia=farmacia).values_list('idReceita')
        # med = MedReceita.objects.filter(idReceita=receita).values_list('nome')

        global dis
        if list(medicamen)==list():
            raise forms.ValidationError('não há esse medicamento na farmácia')

        elif list(a)!=[]:
            receitas = list(a[0])[0]
            if receita in receitas:
                raise forms.ValidationError('Já existe essa receita nessa farmácia.')

        elif list(medicamen)!=list():
            qStock=int(list(medSto[0])[0])
            if qReceita > qStock:
                raise forms.ValidationError('Não há stock suficiente')
            else:
                dis=qStock-qReceita
                Medicamento.objects.values('idFarmacia').filter(idFarmacia=farmacia).values_list('nome').filter(nome=medicamento).update(**{'quantidade': dis})


#------------- adicionar Infarmed -------
class PostForm9(forms.ModelForm):
    class Meta:
        model = Infarmed
        fields = ('nome',)

    def clean(self):
        cleaned_data = super(PostForm9, self).clean()







