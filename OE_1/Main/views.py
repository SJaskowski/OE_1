from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView
from .forms import FormularzPoczatkowy
import random
from django.contrib import messages

# Create your views here.

class MainView(TemplateView):
    def get(self, request, *args, **kwargs):
        formularz=FormularzPoczatkowy()
        contex={
            'formularz':formularz
        }
        return render(self.request, "Strona_glowna.html",contex)
    def post(self,*args,**kwargs):
        formularz = FormularzPoczatkowy(self.request.POST or None)
        if formularz.is_valid():
                zakres1 = formularz.cleaned_data.get('zakres1')
                zakres2 = formularz.cleaned_data.get('zakres2')
                dokladnosc_reprezentacji_chromsomu = formularz.cleaned_data.get('dokladnosc_reprezentacji_chromsomu')
                wielkosc_populacji = formularz.cleaned_data.get('wielkosc_populacji')
                liczba_epok = formularz.cleaned_data.get('liczba_epok')
                metoda_Selekcji = formularz.cleaned_data.get('metoda_Selekcji')
                implementacja_Krzyzowania = formularz.cleaned_data.get('implementacja_Krzyzowania')
                prawdopodbienstwo_Krzyzowania = formularz.cleaned_data.get('prawdopodbienstwo_Krzyzowania')
                implementacja_MutacjiBrzegowej = formularz.cleaned_data.get('rodzaj_platnosci')
                prawdopodbienstwo_MutacjiBrzegowej = formularz.cleaned_data.get('prawdopodbienstwo_MutacjiBrzegowej')
                prawdopodbienstwo_OperatoraInwersji = formularz.cleaned_data.get('prawdopodbienstwo_OperatoraInwersji')
                ile_Przechodzi = formularz.cleaned_data.get('ile_Przechodzi')
                return redirect('Witryna:dokonaj_platnosci')
        else:
            messages.warning(self.request, "Błędnie uzupełniony formularz")
            return render(self.request, "daneAdresowe.html")

def bealeFunction(x1,x2):
    return ((1.5-x1+x1*x2)^2) + ((2.25-x1+x1*x2^2)^2) + (2.625-x1+x1*x2^3)^2


def poczatkoweWartosci(populacja,zakres1,zakres2):
    class individual():
        cecha1=0
        cecha2=0
        wynik=0
    lista= []
    for x in (0,populacja):
        tmp = individual()
        tmp.cecha1=random(zakres1,zakres2)
        tmp.cecha2 = random(zakres1, zakres2)
        tmp.wynik=bealeFunction(tmp.cecha1,tmp.cecha2)
        lista.append(tmp)
    return lista

def selekcjaNajelpszychMAX(ile_najlepszych,populacja=[]):
    licznik=round(ile_najlepszych*populacja.count())
    najelpsze=[]
    i,j = 0
    for i in (0,len(populacja)):
        max=0
        for j in (0,licznik):
            if(populacja[j]>max):
                max=populacja[j]
        populacja.remove(max)
        najelpsze.append(max)
    return najelpsze


def selekcjaNajelpszychMIN(ile_najlepszych,populacja=[]):
    licznik=round(ile_najlepszych*populacja.count())
    najelpsze=[]
    i,j = 0
    for i in (0,len(populacja)):
        min=0
        for j in (0,licznik):
            if(populacja[j]<min):
                min=populacja[j]
        populacja.remove(min)
        najelpsze.append(min)
    return najelpsze

def selecjaTurniejowa():
    pass