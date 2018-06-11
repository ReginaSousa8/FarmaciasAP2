from django.conf.urls import url
from coredrca import views
from django.contrib.auth.decorators import login_required
#from django.views.generic TemplateView

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^medicos$', views.medicos, name='medico'),
    url('cadastro-medicos.html', views.getMedico, name='cad-medicos'),
    url(r'^medicos/(?P<nome>[-\w]+)/$', views.medico_detail, name='infomed'),

    url(r'^utentes$', views.utentes, name='utente'),
    url('cadastro-utentes.html', views.getUtente),
    url(r'^utentes/(?P<nome>[-\w]+)/$', views.utente_detail, name='infoute'),

    url(r'^receitas$', views.receitas, name='receita'),
    url('cadastro-receitas.html', views.getReceita),
url(r'^receitas/(?P<nome>[-\w]+)/$', views.receita_detail, name='inforec'),

    url('cadastro-medrec.html', views.getMedicReceita),

    url(r'^medicamentos$', views.medicamentos, name='medicamento'),
    url('cadastro-medicamentos.html', views.getMedicamento),
    url('addStock.html', views.getMedicStock, name='addstock'),

    url(r'^infarmed$', views.infarmed, name='infarmed'),
    url('cadastro-infarmed.html', views.getInfarmed),

    url(r'^farmacias$', views.farmacias, name='farmacias'),
    url('cadastro-farmacias.html', views.getFarmacia),
    url('addRec.html', views.getRecFarm, name='addreceita'),


    url(r'^deletereceita/(?P<pk>\d+)/$', views.deletereceita, name='deletereceita'),
    url(r'^aviar$', views.aviar, name='aviar'),
]