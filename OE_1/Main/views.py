from Genetic.selection import tournamentSelect,getRouletteWheel,rouletteWheelSelect
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,DetailView
from .forms import FormularzPoczatkowy
from  .models import Wynik,PojedynczaWartoscWyniku,Ustawienia
import random,math
from django.contrib import messages
from django.utils import timezone
import statistics



# Create your views here. TODO Wyswietlanie wynikow

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
                rodzaj_Optymalizacj=formularz.cleaned_data.get('rodzaj_Optymalizacj')
                ustawienia=Ustawienia(
                    zakres1 = zakres1,
                    zakres2 = zakres2,
                    dokladnosc = dokladnosc_reprezentacji_chromsomu,
                    wielkoscPopulacji = wielkosc_populacji,
                    liczbaepok = liczba_epok,
                    metodaSelekcji = metoda_Selekcji,
                    implementacjaKrzyzowania = implementacja_Krzyzowania,
                    prawdobodobienstwoKrzyzowania = prawdopodbienstwo_Krzyzowania,
                    implementacjaMutowania = implementacja_MutacjiBrzegowej,
                    prawdobodobienstwoMutowania = prawdopodbienstwo_MutacjiBrzegowej,
                    prawdobodobienstwoinwersji = prawdopodbienstwo_OperatoraInwersji,
                    ileprzechodzi = ile_Przechodzi,
                    rodzaj_Optymalizacj=rodzaj_Optymalizacj
                )
                licz(ustawienia)
                return redirect('Main:wynik')
        else:
            messages.warning(self.request, "Błędnie uzupełniony formularz")
            return render(self.request, "daneAdresowe.html")



class WynikDzialania(TemplateView):
   model = Ustawienia
   template_name = "Obliczenia.html"


def binarnaReprezentacja(zakres1, zakres2, dokladnosc, liczba):
    dlugoscLancucha = math.ceil(math.log(((zakres2 - zakres1) * pow(10, dokladnosc)), 2) + math.log(1, 2))
    if str(liczba).count(".") == 1:
        czescCalkowita, czescDziesetna = str(liczba).split(".")
        czescCalkowita = int(czescCalkowita)
        czescDziesetna = int(czescDziesetna)
        res = bin(czescCalkowita).lstrip("0b") + "."

        def decimal_converter(num):
            while num > 1:
                num /= 10
            return num

        for x in range((dlugoscLancucha - bin(czescCalkowita).__len__()) + 2):
            czescCalkowita, czescDziesetna = str((decimal_converter(czescDziesetna)) * 2).split(".")
            czescDziesetna = int(czescDziesetna)
            res += czescCalkowita
    else:
        res = bin(liczba).lstrip("0b") + "."
        for x in range((dlugoscLancucha - bin(liczba).__len__()) + 2):
            res += "0"
    if(liczba>0):
        res = "0" + res
    else:
        res = "1" + res
    return res

def dziesietnaReprezentacja(liczba):
        if(liczba[0] == "1"):
            liczba=liczba[1:liczba.__len__()]
            czescCalkowita, czescDziesetna = str(liczba).split(".")
            czescCalkowita = "0b" + str(czescCalkowita)
            czescCalkowita = int(czescCalkowita, 2)
            res = czescCalkowita
            for x in range(1, czescDziesetna.__len__() + 1):
                res += float(czescDziesetna[x - 1]) / pow(2, x)
            return res*-1
        else:
            czescCalkowita, czescDziesetna = str(liczba).split(".")
            czescCalkowita = "0b" + str(czescCalkowita)
            czescCalkowita = int(czescCalkowita, 2)
            res = czescCalkowita
            for x in range(1, czescDziesetna.__len__() + 1):
                res += float(czescDziesetna[x - 1]) / pow(2, x)
            return res

class individual():
    cecha1 = 0
    cecha2 = 0
    wynik = 0


def bealeFunction(x1,x2):
    return ((1.5-x1+x1*x2)^2) + ((2.25-x1+x1*x2^2)^2) + (2.625-x1+x1*x2^3)^2


def poczatkoweWartosci(populacja,zakres1,zakres2):
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


def selekcjaNajelpszychMIN(ile_najlepszych, populacja=[]):
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


def selecjaTurniejowa(iloscZwyciezcow, wielkoscTurnieju, populacja=[]):
    iloscTurniejow = populacja.__len__() / wielkoscTurnieju
    return tournamentSelect(populacja,wielkoscTurnieju,iloscZwyciezcow)


def selekcjaKolemRuletki(populacja=[]):
    return rouletteWheelSelect(getRouletteWheel(populacja))


def implementacjaKrzyzowania(typ, zakres1, zakres2, dokladnosc, populacja=[]):
    nowePokolenie=[]
    if typ=="JP": # Krzyzowanie jednopuknotowe
        for x in range(populacja.__len__()):
            punktKrzyzowania = random(1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__() - 1)
            if populacja[x+1]!=object(): #Krzyzowanie Ostatniego osbonika z populacji z pierwszym
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
                chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
                chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
                potomek1cecha1 = chromosom1cecha1bin
                potomek1cecha2 = chromosom1cecha2bin
                for i in range(punktKrzyzowania, chromosom1cecha1bin):
                    potomek1cecha1[i] = chromosom2cecha1bin[i]
                for i in range(punktKrzyzowania, chromosom1cecha2bin):
                    potomek1cecha2[i] = chromosom2cecha2bin[i]
                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
                tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)
            chromosom1cecha1bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x].cecha1)
            chromosom1cecha2bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x].cecha2)
            chromosom2cecha1bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x+1].cecha1)
            chromosom2cecha2bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x+1].cecha2)
            potomek1cecha1 = chromosom1cecha1bin
            potomek1cecha2 = chromosom1cecha2bin
            for i in range(punktKrzyzowania,chromosom1cecha1bin):
                potomek1cecha1[i]=chromosom2cecha1bin[i]
            for i in range(punktKrzyzowania,chromosom1cecha2bin):
                potomek1cecha2[i]=chromosom2cecha2bin[i]
            tmp = individual()
            tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
            tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)

    if typ=="DP":
        for x in range(populacja.__len__()):
            punktKrzyzowania = random(1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__() - 2)
            punktKrzyzowania2 = random(punktKrzyzowania+1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__() - 1)
            if populacja[x+1]!=object(): #Krzyzowanie Ostatniego osbonika z populacji z pierwszym
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
                chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
                chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
                potomek1cecha1 = chromosom1cecha1bin
                potomek1cecha2 = chromosom1cecha2bin
                for i in range(punktKrzyzowania, punktKrzyzowania2):
                    potomek1cecha1[i] = chromosom2cecha1bin[i]
                for i in range(punktKrzyzowania, punktKrzyzowania2):
                    potomek1cecha2[i] = chromosom2cecha2bin[i]
                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
                tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)
            chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
            chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
            chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x + 1].cecha1)
            chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x + 1].cecha2)
            potomek1cecha1 = chromosom1cecha1bin
            potomek1cecha2 = chromosom1cecha2bin
            for i in range(punktKrzyzowania, punktKrzyzowania2):
                potomek1cecha1[i] = chromosom2cecha1bin[i]
            for i in range(punktKrzyzowania, punktKrzyzowania2):
                potomek1cecha2[i] = chromosom2cecha2bin[i]
            tmp = individual()
            tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
            tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)
    if typ=="TP":
     for x in range(populacja.__len__()):
         punktKrzyzowania = random(1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                               populacja[x].cecha1).__len__() - 2)
         punktKrzyzowania2 = random(punktKrzyzowania + 1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                               populacja[x].cecha1).__len__() - 4)
         punktKrzyzowania3 = random(punktKrzyzowania2 + 1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                               populacja[x].cecha1).__len__() - 1)
         if populacja[x + 1] != object():  # Krzyzowanie Ostatniego osbonika z populacji z pierwszym
             chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
             chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
             chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
             chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
             potomek1cecha1 = chromosom1cecha1bin
             potomek1cecha2 = chromosom1cecha2bin
             for i in range(punktKrzyzowania, punktKrzyzowania2):
                 potomek1cecha1[i] = chromosom2cecha1bin[i]
             for i in range(punktKrzyzowania3, chromosom1cecha1bin.__len__()):
                 potomek1cecha1[i] = chromosom2cecha1bin[i]
             for i in range(punktKrzyzowania, punktKrzyzowania2):
                 potomek1cecha2[i] = chromosom2cecha2bin[i]
             for i in range(punktKrzyzowania3, chromosom1cecha2bin.__len__()):
                 potomek1cecha2[i] = chromosom2cecha2bin[i]
             tmp = individual()
             tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
             tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
             tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
             nowePokolenie.append(tmp)

    if typ=="JJ":
     for x in range(populacja.__len__()):
         if populacja[x + 1] != object():  # Krzyzowanie Ostatniego osbonika z populacji z pierwszym
             chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
             chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
             chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
             chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
             potomek1cecha1 = chromosom1cecha1bin
             potomek1cecha2 = chromosom1cecha2bin
             for i in range(chromosom1cecha1bin):
                 if i%2 == 1:
                     potomek1cecha1[i] = chromosom2cecha1bin[i]
             for i in range(punktKrzyzowania, punktKrzyzowania2):
                 if i % 2 == 1:
                     potomek1cecha2[i] = chromosom2cecha2bin[i]
             tmp = individual()
             tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
             tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
             tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
             nowePokolenie.append(tmp)
         chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
         chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
         chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x+1].cecha1)
         chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x+1].cecha2)
         potomek1cecha1 = chromosom1cecha1bin
         potomek1cecha2 = chromosom1cecha2bin
         for i in range(chromosom1cecha1bin):
             if i % 2 == 1:
                 potomek1cecha1[i] = chromosom2cecha1bin[i]
         for i in range(punktKrzyzowania, punktKrzyzowania2):
             if i % 2 == 1:
                 potomek1cecha2[i] = chromosom2cecha2bin[i]
         tmp = individual()
         tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
         tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
         tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
         nowePokolenie.append(tmp)
    return nowePokolenie


def implementacjaMutacji(typ,prawdobodobienstwo, zakres1, zakres2, dokladnosc,populacja=[]):
    nowePokolenie=[]
    if typ == "MB":
        for x in populacja:
            if random(0,100)<=prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)

                if chromosom1cecha1bin[chromosom1cecha1bin.__len__()] == "0":
                    chromosom1cecha1bin[chromosom1cecha1bin.__len__()] = "1"
                else:
                    chromosom1cecha1bin[chromosom1cecha1bin.__len__()] = "0"

                if chromosom1cecha2bin[chromosom1cecha2bin.__len__()] == "0":
                    chromosom1cecha2bin[chromosom1cecha2bin.__len__()]= "1"
                else:
                    chromosom1cecha2bin[chromosom1cecha2bin.__len__()] = "0"

                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(chromosom1cecha1bin)
                tmp.cecha2 = dziesietnaReprezentacja(chromosom1cecha2bin)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)

            else:
                nowePokolenie.append(x)
    if typ == "JP":
        for x in populacja:
            if random(0, 100) <= prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
                punktMutacji = random(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                  populacja[x].cecha1).__len__())
                if chromosom1cecha1bin[punktMutacji] == "0":
                    chromosom1cecha1bin[punktMutacji] = "1"
                else:
                    chromosom1cecha1bin[punktMutacji] = "0"
                if chromosom1cecha2bin[punktMutacji] == "0":
                    chromosom1cecha2bin[punktMutacji] = "1"
                else:
                    chromosom1cecha2bin[punktMutacji] = "0"


                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(chromosom1cecha1bin)
                tmp.cecha2 = dziesietnaReprezentacja(chromosom1cecha2bin)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)

        else:
                nowePokolenie.append(x)
    if typ == "DP":
        for x in populacja:
            if random(0, 100) <= prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
                punktMutacji = random(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__())
                punktMutacji2 = random(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__())
                while punktMutacji2 == punktMutacji:
                    punktMutacji2 = random(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                   populacja[x].cecha1).__len__())
                if chromosom1cecha1bin[punktMutacji] == "0":
                    chromosom1cecha1bin[punktMutacji] = "1"
                else:
                    chromosom1cecha1bin[punktMutacji] = "0"

                if chromosom1cecha2bin[punktMutacji] == "0":
                    chromosom1cecha2bin[punktMutacji] = "1"
                else:
                    chromosom1cecha2bin[punktMutacji] = "0"

                if chromosom1cecha1bin[punktMutacji2] == "0":
                    chromosom1cecha1bin[punktMutacji2] = "1"
                else:
                    chromosom1cecha1bin[punktMutacji2] = "0"
                if chromosom1cecha2bin[punktMutacji2] == "0":
                    chromosom1cecha2bin[punktMutacji2] = "1"
                else:
                    chromosom1cecha2bin[punktMutacji2] = "0"

                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(chromosom1cecha1bin)
                tmp.cecha2 = dziesietnaReprezentacja(chromosom1cecha2bin)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)
            else:
                nowePokolenie.append(x)
    return nowePokolenie

def implementacjaInwersji(prawdobodobienstwo, zakres1, zakres2, dokladnosc,populacja=[]):
    nowePokolenie=[]
    for x in populacja :
        if random(0, 100) <= prawdobodobienstwo:
            punktinwersji1 = random(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__() - 2)
            punktinwersji2 = random(punktinwersji1 , binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                                  populacja[x].cecha1).__len__() - 1)

            chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
            chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
            potomek1cecha1 = chromosom1cecha1bin
            potomek1cecha2 = chromosom1cecha2bin
            for i in range(punktinwersji1, punktinwersji2):
                if potomek1cecha1[i] == "0":
                    potomek1cecha1[i] = "1"
                else:
                    potomek1cecha1[i] = "0"
            for i in range(punktinwersji1, punktinwersji2):
                if potomek1cecha2[i] == "0":
                    potomek1cecha2[i] = "1"
                else:
                    potomek1cecha2[i] = "0"
            tmp = individual()
            tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
            tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)
        else:
            nowePokolenie.append(x)

    return nowePokolenie


def licz(ustawienia):
    populacja=poczatkoweWartosci(ustawienia.wielkoscPopulacji,ustawienia.zakres1,ustawienia.zakres2)

    for i in range(ustawienia.liczbaepok):
        if ustawienia.metodaSelekcji== "SN":
            if(ustawienia.rodzaj_Optymalizacj=="Min"):
                populacja=selekcjaNajelpszychMIN(ustawienia.ileprzechodzi,populacja)
                if random(0,100)<=ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania,ustawienia.zakres1, ustawienia.zakres2,ustawienia.dokladnosc,populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,ustawienia.prawdobodobienstwoMutowania,ustawienia.zakres1, ustawienia.zakres2,ustawienia.dokladnosc,populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc, populacja)
            else:
                populacja = selekcjaNajelpszychMAX(ustawienia.ileprzechodzi, populacja)
                if random(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                         ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                 ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                  ustawienia.zakres2, ustawienia.dokladnosc, populacja)
        else:
            if ustawienia.metodaSelekcji== "SR":
                populacja = selekcjaKolemRuletki(populacja)
                if random(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                         ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                 ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                  ustawienia.zakres2, ustawienia.dokladnosc, populacja)
            else:
                if ustawienia.metodaSelekcji == "ST":
                    populacja = selecjaTurniejowa(ustawienia.ileprzechodzi, populacja)
                    if random(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                        populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                             ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                    populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                     ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                     ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                    populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                      ustawienia.zakres2, ustawienia.dokladnosc, populacja)

    wyniki_epoki = Wynik(
        czas= timezone.now(),
        iteracja = i

    )
    sredniwynik = 0
    listawynikow=[]
    for x in populacja:
        wynik=PojedynczaWartoscWyniku(
        wartosc = x.wynik,
        x1 = x.cecha1,
        x2 = x.cecha2
        )
        wyniki_epoki.wyniki.add(wynik)
        listawynikow.append(wynik.wartosc)
        sredniwynik+=wynik.wartosc
    wyniki_epoki.sredniwynik=sredniwynik/populacja.count()
    wyniki_epoki.odchyleniestandardowe=statistics.stdev(listawynikow)
    wyniki_epoki.save()
