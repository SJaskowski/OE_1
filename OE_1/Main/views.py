from Genetic.selection import tournamentSelect,getRouletteWheel,rouletteWheelSelect
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,DetailView,ListView
from .forms import FormularzPoczatkowy
from  .models import Epoka,PojedynczaWartoscWyniku,Ustawienia,Wynik
from django.contrib import messages
from django.utils import timezone
import statistics,math,random
from




# Create your views here. TODO Wyswietlanie wynikow do funkcji/klasyy




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
                implementacja_MutacjiBrzegowej = formularz.cleaned_data.get('implementacja_MutacjiBrzegowej')
                prawdopodbienstwo_MutacjiBrzegowej = formularz.cleaned_data.get('prawdopodbienstwo_MutacjiBrzegowej')
                prawdopodbienstwo_OperatoraInwersji = formularz.cleaned_data.get('prawdopodbienstwo_OperatoraInwersji')
                ile_Przechodzi = formularz.cleaned_data.get('ile_Przechodzi')
                rodzaj_Optymalizacj=formularz.cleaned_data.get('rodzaj_Optymalizacj')
                ID_Wyniku= formularz.cleaned_data.get('ID_Wyniku')
                ustawienia=Ustawienia.objects.create(
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
                    rodzaj_Optymalizacj=rodzaj_Optymalizacj,
                    ID_Wyniku=ID_Wyniku

                )
                licz(ustawienia)
                return redirect('Main:wynik',ustawienia.ID_Wyniku)
        else:
            messages.warning(self.request, "Błędnie uzupełniony formularz")
            return render(self.request, "daneAdresowe.html")



class WynikDzialania(ListView):
    model = Epoka

    def get_context_data(self, **kwargs):
        id_wyniku = self.request.path.rsplit("/")
        id_wyniku=id_wyniku[-1]
        Wyniki = Wynik.objects.filter(id=id_wyniku)
        context = {"Epoka":Wyniki[0].epoka_set.all()}
        return context
    template_name = "Obliczenia.html"


def binarnaReprezentacja(zakres1, zakres2, dokladnosc, liczba):
    dlugoscLancucha = math.ceil(math.log(((zakres2 - zakres1) * pow(10, dokladnosc)), 2) + math.log(1, 2))
    if str(liczba).count(".") == 1:

        czescCalkowita, czescDziesetna = str(liczba).split(".")
        czescCalkowita = int(czescCalkowita)
        czescDziesetna="0."+czescDziesetna
        czescDziesetna = float(czescDziesetna)
        res = bin(czescCalkowita).lstrip("0b") + "."

        for x in range(dlugoscLancucha - res.__len__()):

            # Find next bit in fraction
            czescDziesetna *= 2
            fract_bit = int(czescDziesetna)

            if (fract_bit == 1):

                czescDziesetna -= fract_bit
                res += '1'

            else:
                res += '0'


    else:
        res = bin(liczba).lstrip("-0b") + "."
        for x in range((dlugoscLancucha - bin(liczba).__len__()) + 2):
            res += "0"
    if (liczba > 0):
        while res.__len__() < dlugoscLancucha:
            res += '0'
        res = "0" + res
    else:
        res = res.lstrip("-0b")
        while res.__len__() < dlugoscLancucha:
            res += '0'
        res = "1" + res
    return res

def dziesietnaReprezentacja(liczba):
        if(liczba[0] == "1"):
            liczba=liczba[1:liczba.__len__()]
            czescCalkowita, czescDziesetna = str(liczba).split(".")
            if czescCalkowita != "":
                czescCalkowita = int(czescCalkowita, 2)
            else:
                czescCalkowita = 0
            res = czescCalkowita
            for x in range(1, czescDziesetna.__len__() + 1):
                res += float(czescDziesetna[x - 1]) / pow(2, x)
            return res*-1
        else:
            czescCalkowita, czescDziesetna = str(liczba).split(".")
            if czescCalkowita != "":
                czescCalkowita = int(czescCalkowita, 2)
            else:
                czescCalkowita = 0
            res = czescCalkowita
            for x in range(1, czescDziesetna.__len__() + 1):
                res += float(czescDziesetna[x - 1]) / pow(2, x)
            return res

class individual():
    cecha1 = 0
    cecha2 = 0
    wynik = 0


def bealeFunction(x1,x2):
    return pow((1.5-x1+x1*x2), 2) + pow((2.25-x1+x1*pow(x2,2)), 2) + pow((2.625-x1+x1*pow(x2, 3)),2)


def poczatkoweWartosci(populacja,zakres1,zakres2):
    lista= []
    for x in range(0,populacja):
        tmp = individual()
        tmp.cecha1=random.uniform(zakres1,zakres2)
        tmp.cecha2 = random.uniform(zakres1, zakres2)
        tmp.wynik=bealeFunction(tmp.cecha1,tmp.cecha2)
        lista.append(tmp)
    return lista


def selekcjaNajelpszychMAX(ile_najlepszych,populacja=[]):
    licznik=round(ile_najlepszych*populacja.__len__())
    najelpsze=[]
    i = 0
    j = 0
    for i in (0,len(populacja)):
        max=0
        for j in (0,licznik):
            if(populacja[i].wynik>max):
                max=populacja[i].wynik
                individual=populacja[i]
            populacja.remove(individual)
            najelpsze.append(individual)
    return najelpsze


def selekcjaNajelpszychMIN(ile_najlepszych, populacja=[]):
    licznik=round(ile_najlepszych*populacja.count())
    najelpsze=[]
    i = 0
    j = 0
    for i in (0,len(populacja)):
        min=0
        for j in (0,licznik):
            if(populacja[j].wynik<min):
                min=populacja[j].wynik
        populacja.remove(min)
        najelpsze.append(min)
    return najelpsze


def selecjaTurniejowa(iloscZwyciezcow, wielkoscTurnieju, populacja=[]):
    return tournamentSelect(populacja,wielkoscTurnieju,iloscZwyciezcow)


def selekcjaKolemRuletki(populacja=[]):
    score={}
    najlepsi=[]
    for indiv in populacja:
        score.update({indiv:indiv.wynik})
    for x in range(0,populacja.__len__()):
     najlepsi.append(rouletteWheelSelect(getRouletteWheel(populacja,score)))
    return najlepsi


def implementacjaKrzyzowania(typ, zakres1, zakres2, dokladnosc, populacja=[]):
    nowePokolenie=[]
    if typ=="JP": # Krzyzowanie jednopuknotowe
        for x in range(populacja.__len__()):
            punktKrzyzowania = random.randint(1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__() - 1)

            if x==populacja.__len__()-1: #Krzyzowanie Ostatniego osbonika z populacji z pierwszym

                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
                chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
                chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
                potomek1cecha1 = chromosom1cecha1bin
                potomek1cecha2 = chromosom1cecha2bin



                dot1 = potomek1cecha1.find(".")
                potomek1cecha1 = list(potomek1cecha1)
                potomek1cecha1.pop(dot1)
                potomek1cecha1 = "".join(potomek1cecha1)
                dot2 = chromosom2cecha1bin.find(".")
                chromosom2cecha1bin = list(chromosom2cecha1bin)
                chromosom2cecha1bin.pop(dot2)
                chromosom2cecha1bin = "".join(chromosom2cecha1bin)
                dot3 = potomek1cecha2.find(".")
                potomek1cecha2 = list(potomek1cecha2)
                potomek1cecha2.pop(dot3)
                potomek1cecha2 = "".join(potomek1cecha2)
                dot4 = chromosom2cecha2bin.find(".")
                chromosom2cecha2bin = list(chromosom2cecha2bin)
                chromosom2cecha2bin.pop(dot4)
                chromosom2cecha2bin = "".join(chromosom2cecha2bin)


                for i in range(punktKrzyzowania, chromosom2cecha1bin.__len__()-1):

                        potomek1cecha1=list(potomek1cecha1)
                        potomek1cecha1[i] = chromosom2cecha1bin[i]
                        potomek1cecha1="".join(potomek1cecha1)


                for i in range(punktKrzyzowania, chromosom2cecha2bin.__len__()-1):

                        potomek1cecha2 = list(potomek1cecha2)
                        potomek1cecha2[i] = chromosom2cecha2bin[i]
                        potomek1cecha2 = "".join(potomek1cecha2)

                if dot1 != dot2:
                    if dot1 > dot2:
                        newdot1 = random.randint(dot2, dot1)
                    else:
                        newdot1 = random.randint(dot1, dot2)
                else:
                    newdot1 = dot1
                if dot3 != dot4:
                    if dot3 > dot4:
                        newdot2 = random.randint(dot4, dot3)
                    else:
                        newdot2 = random.randint(dot3, dot4)
                else:
                    newdot2 = dot2

                potomek1cecha1 = list(potomek1cecha1)
                potomek1cecha1.insert(newdot1,".")
                potomek1cecha1 = "".join(potomek1cecha1)

                potomek1cecha2 = list(potomek1cecha2)
                potomek1cecha2.insert(newdot2,".")
                potomek1cecha2 = "".join(potomek1cecha2)

                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
                tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)
                break



            chromosom1cecha1bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x].cecha1)
            chromosom1cecha2bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x].cecha2)
            chromosom2cecha1bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x+1].cecha1)
            chromosom2cecha2bin = binarnaReprezentacja(zakres1,zakres2,dokladnosc,populacja[x+1].cecha2)

            potomek1cecha1 = chromosom1cecha1bin
            potomek1cecha2 = chromosom1cecha2bin

            dot1 = potomek1cecha1.find(".")
            potomek1cecha1 = list(potomek1cecha1)
            potomek1cecha1.pop(dot1)
            potomek1cecha1 = "".join(potomek1cecha1)
            dot2 = chromosom2cecha1bin.find(".")
            chromosom2cecha1bin = list(chromosom2cecha1bin)
            chromosom2cecha1bin.pop(dot2)
            chromosom2cecha1bin = "".join(chromosom2cecha1bin)
            dot3 = potomek1cecha2.find(".")
            potomek1cecha2 = list(potomek1cecha2)
            potomek1cecha2.pop(dot3)
            potomek1cecha2 = "".join(potomek1cecha2)
            dot4 = chromosom2cecha2bin.find(".")
            chromosom2cecha2bin = list(chromosom2cecha2bin)
            chromosom2cecha2bin.pop(dot4)
            chromosom2cecha2bin = "".join(chromosom2cecha2bin)

            for i in range(punktKrzyzowania, chromosom2cecha1bin.__len__() - 1):
                potomek1cecha1 = list(potomek1cecha1)
                potomek1cecha1[i] = chromosom2cecha1bin[i]
                potomek1cecha1 = "".join(potomek1cecha1)

            for i in range(punktKrzyzowania, chromosom2cecha2bin.__len__() - 1):
                potomek1cecha2 = list(potomek1cecha2)
                potomek1cecha2[i] = chromosom2cecha2bin[i]
                potomek1cecha2 = "".join(potomek1cecha2)

            if dot1 != dot2:
                if dot1 > dot2:
                    newdot1 = random.randint(dot2, dot1)
                else:
                    newdot1 = random.randint(dot1, dot2)
            else:
                newdot1=dot1
            if dot3 != dot4:
                if dot3 > dot4:
                    newdot2 = random.randint(dot4, dot3)
                else:
                    newdot2 = random.randint(dot3, dot4)
            else:
                newdot2=dot2

            potomek1cecha1 = list(potomek1cecha1)
            potomek1cecha1.insert(newdot1, ".")
            potomek1cecha1 = "".join(potomek1cecha1)

            potomek1cecha2 = list(potomek1cecha2)
            potomek1cecha2.insert(newdot2, ".")
            potomek1cecha2 = "".join(potomek1cecha2)

            tmp = individual()
            tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
            tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)


    if typ=="DP":
        for x in range(populacja.__len__()):
            punktKrzyzowania = random.randint(1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__() - 4)
            if binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 2 == punktKrzyzowania+1:
                punktKrzyzowania2 = random.randint(punktKrzyzowania+1, binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 2)
            else:
                punktKrzyzowania2 = random.randint(punktKrzyzowania+2, binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 2)

            if x==populacja.__len__()-1: #Krzyzowanie Ostatniego osbonika z populacji z pierwszym
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
                chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
                chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
                if chromosom1cecha1bin.__len__() != chromosom1cecha2bin.__len__():
                    print("-----------------------")
                    print(chromosom1cecha1bin.__len__())
                    print(chromosom1cecha2bin.__len__())
                    print(populacja[x].cecha1)
                    print(populacja[x].cecha2)
                potomek1cecha1 = chromosom1cecha1bin
                potomek1cecha2 = chromosom1cecha2bin

                dot1 = potomek1cecha1.find(".")
                potomek1cecha1 = list(potomek1cecha1)
                potomek1cecha1.pop(dot1)
                potomek1cecha1 = "".join(potomek1cecha1)
                dot2 = chromosom2cecha1bin.find(".")
                chromosom2cecha1bin = list(chromosom2cecha1bin)
                chromosom2cecha1bin.pop(dot2)
                chromosom2cecha1bin = "".join(chromosom2cecha1bin)
                dot3 = potomek1cecha2.find(".")
                potomek1cecha2 = list(potomek1cecha2)
                potomek1cecha2.pop(dot3)
                potomek1cecha2 = "".join(potomek1cecha2)
                dot4 = chromosom2cecha2bin.find(".")
                chromosom2cecha2bin = list(chromosom2cecha2bin)
                chromosom2cecha2bin.pop(dot4)
                chromosom2cecha2bin = "".join(chromosom2cecha2bin)

                for i in range(punktKrzyzowania, punktKrzyzowania2):
                    potomek1cecha1 = list(potomek1cecha1)
                    potomek1cecha1[i] = chromosom2cecha1bin[i]
                    potomek1cecha1 = "".join(potomek1cecha1)
                for i in range(punktKrzyzowania, punktKrzyzowania2):
                    potomek1cecha2 = list(potomek1cecha2)
                    potomek1cecha2[i] = chromosom2cecha2bin[i]
                    potomek1cecha2 = "".join(potomek1cecha2)
                if dot1 != dot2:
                    if dot1 > dot2:
                        newdot1 = random.randint(dot2, dot1)
                    else:
                        newdot1 = random.randint(dot1, dot2)
                else:
                    newdot1 = dot1
                if dot3 != dot4:
                    if dot3 > dot4:
                        newdot2 = random.randint(dot4, dot3)
                    else:
                        newdot2 = random.randint(dot3, dot4)
                else:
                    newdot2 = dot2

                potomek1cecha1 = list(potomek1cecha1)
                potomek1cecha1.insert(newdot1, ".")
                potomek1cecha1 = "".join(potomek1cecha1)

                potomek1cecha2 = list(potomek1cecha2)
                potomek1cecha2.insert(newdot2, ".")
                potomek1cecha2 = "".join(potomek1cecha2)

                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
                tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)
                break

            chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
            chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
            chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x + 1].cecha1)
            chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x + 1].cecha2)
            potomek1cecha1 = chromosom1cecha1bin
            potomek1cecha2 = chromosom1cecha2bin

            dot1 = potomek1cecha1.find(".")
            potomek1cecha1 = list(potomek1cecha1)
            potomek1cecha1.pop(dot1)
            potomek1cecha1 = "".join(potomek1cecha1)
            dot2 = chromosom2cecha1bin.find(".")
            chromosom2cecha1bin = list(chromosom2cecha1bin)
            chromosom2cecha1bin.pop(dot2)
            chromosom2cecha1bin = "".join(chromosom2cecha1bin)
            dot3 = potomek1cecha2.find(".")
            potomek1cecha2 = list(potomek1cecha2)
            potomek1cecha2.pop(dot3)
            potomek1cecha2 = "".join(potomek1cecha2)
            dot4 = chromosom2cecha2bin.find(".")
            chromosom2cecha2bin = list(chromosom2cecha2bin)
            chromosom2cecha2bin.pop(dot4)
            chromosom2cecha2bin = "".join(chromosom2cecha2bin)

            for i in range(punktKrzyzowania, punktKrzyzowania2):
                potomek1cecha1 = list(potomek1cecha1)
                potomek1cecha1[i] = chromosom2cecha1bin[i]
                potomek1cecha1 = "".join(potomek1cecha1)
            for i in range(punktKrzyzowania, punktKrzyzowania2):
                potomek1cecha2 = list(potomek1cecha2)
                potomek1cecha2[i] = chromosom2cecha2bin[i]
                potomek1cecha2 = "".join(potomek1cecha2)
            if dot1 != dot2:
                if dot1 > dot2:
                    newdot1 = random.randint(dot2, dot1)
                else:
                    newdot1 = random.randint(dot1, dot2)
            else:
                newdot1 = dot1
            if dot3 != dot4:
                if dot3 > dot4:
                    newdot2 = random.randint(dot4, dot3)
                else:
                    newdot2 = random.randint(dot3, dot4)
            else:
                newdot2 = dot2

            potomek1cecha1 = list(potomek1cecha1)
            potomek1cecha1.insert(newdot1, ".")
            potomek1cecha1 = "".join(potomek1cecha1)

            potomek1cecha2 = list(potomek1cecha2)
            potomek1cecha2.insert(newdot2, ".")
            potomek1cecha2 = "".join(potomek1cecha2)

            tmp = individual()
            tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
            tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)

    if typ=="TP":
     for x in range(populacja.__len__()):
         punktKrzyzowania = random.randint(1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                               populacja[x].cecha1).__len__() - 8)
         if punktKrzyzowania + 1 == binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 4 :
            punktKrzyzowania2 = random.randint(punktKrzyzowania + 2, binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 6)
         else:
             punktKrzyzowania2 = random.randint(punktKrzyzowania + 1, binarnaReprezentacja(zakres1, zakres2, dokladnosc,populacja[x].cecha1).__len__() - 6)
         if punktKrzyzowania2 + 1 == binarnaReprezentacja(zakres1, zakres2, dokladnosc,populacja[x].cecha1).__len__() - 1 :
             punktKrzyzowania3 = random.randint(punktKrzyzowania2 + 2, binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 1)
         else:
             punktKrzyzowania3 = random.randint(punktKrzyzowania2 + 1,binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1).__len__() - 1)

         if x==populacja.__len__()-1:  # Krzyzowanie Ostatniego osbonika z populacji z pierwszym
             chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
             chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
             chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
             chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
             potomek1cecha1 = chromosom1cecha1bin
             potomek1cecha2 = chromosom1cecha2bin

             dot1 = potomek1cecha1.find(".")
             potomek1cecha1 = list(potomek1cecha1)
             potomek1cecha1.pop(dot1)
             potomek1cecha1 = "".join(potomek1cecha1)
             dot2 = chromosom2cecha1bin.find(".")
             chromosom2cecha1bin = list(chromosom2cecha1bin)
             chromosom2cecha1bin.pop(dot2)
             chromosom2cecha1bin = "".join(chromosom2cecha1bin)
             dot3 = potomek1cecha2.find(".")
             potomek1cecha2 = list(potomek1cecha2)
             potomek1cecha2.pop(dot3)
             potomek1cecha2 = "".join(potomek1cecha2)
             dot4 = chromosom2cecha2bin.find(".")
             chromosom2cecha2bin = list(chromosom2cecha2bin)
             chromosom2cecha2bin.pop(dot4)
             chromosom2cecha2bin = "".join(chromosom2cecha2bin)

             for i in range(punktKrzyzowania, punktKrzyzowania2):
                 potomek1cecha1 = list(potomek1cecha1)
                 potomek1cecha1[i] = chromosom2cecha1bin[i]
                 potomek1cecha1 = "".join(potomek1cecha1)
             for i in range(punktKrzyzowania3, chromosom1cecha1bin.__len__()-1):
                 potomek1cecha1 = list(potomek1cecha1)
                 potomek1cecha1[i] = chromosom2cecha1bin[i]
                 potomek1cecha1 = "".join(potomek1cecha1)
             for i in range(punktKrzyzowania, punktKrzyzowania2):
                 potomek1cecha2 = list(potomek1cecha2)
                 potomek1cecha2[i] = chromosom2cecha2bin[i]
                 potomek1cecha2 = "".join(potomek1cecha2)
             for i in range(punktKrzyzowania3, chromosom1cecha2bin.__len__()-1):
                 potomek1cecha2 = list(potomek1cecha2)
                 potomek1cecha2[i] = chromosom2cecha2bin[i]
                 potomek1cecha2 = "".join(potomek1cecha2)

             if dot1 != dot2:
                 if dot1 > dot2:
                     newdot1 = random.randint(dot2, dot1)
                 else:
                     newdot1 = random.randint(dot1, dot2)
             else:
                 newdot1 = dot1
             if dot3 != dot4:
                 if dot3 > dot4:
                     newdot2 = random.randint(dot4, dot3)
                 else:
                     newdot2 = random.randint(dot3, dot4)
             else:
                 newdot2 = dot2

             potomek1cecha1 = list(potomek1cecha1)
             potomek1cecha1.insert(newdot1, ".")
             potomek1cecha1 = "".join(potomek1cecha1)

             potomek1cecha2 = list(potomek1cecha2)
             potomek1cecha2.insert(newdot2, ".")
             potomek1cecha2 = "".join(potomek1cecha2)

             tmp = individual()
             tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
             tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
             tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
             nowePokolenie.append(tmp)
             break

         chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
         chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
         chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x+1].cecha1)
         chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x+1].cecha2)
         potomek1cecha1 = chromosom1cecha1bin
         potomek1cecha2 = chromosom1cecha2bin

         dot1 = potomek1cecha1.find(".")
         potomek1cecha1 = list(potomek1cecha1)
         potomek1cecha1.pop(dot1)
         potomek1cecha1 = "".join(potomek1cecha1)
         dot2 = chromosom2cecha1bin.find(".")
         chromosom2cecha1bin = list(chromosom2cecha1bin)
         chromosom2cecha1bin.pop(dot2)
         chromosom2cecha1bin = "".join(chromosom2cecha1bin)
         dot3 = potomek1cecha2.find(".")
         potomek1cecha2 = list(potomek1cecha2)
         potomek1cecha2.pop(dot3)
         potomek1cecha2 = "".join(potomek1cecha2)
         dot4 = chromosom2cecha2bin.find(".")
         chromosom2cecha2bin = list(chromosom2cecha2bin)
         chromosom2cecha2bin.pop(dot4)
         chromosom2cecha2bin = "".join(chromosom2cecha2bin)

         for i in range(punktKrzyzowania, punktKrzyzowania2):
             potomek1cecha1 = list(potomek1cecha1)
             potomek1cecha1[i] = chromosom2cecha1bin[i]
             potomek1cecha1 = "".join(potomek1cecha1)
         for i in range(punktKrzyzowania3, chromosom2cecha1bin.__len__() - 1):
             potomek1cecha1 = list(potomek1cecha1)
             potomek1cecha1[i] = chromosom2cecha1bin[i]
             potomek1cecha1 = "".join(potomek1cecha1)
         for i in range(punktKrzyzowania, punktKrzyzowania2):
             potomek1cecha2 = list(potomek1cecha2)
             potomek1cecha2[i] = chromosom2cecha2bin[i]
             potomek1cecha2 = "".join(potomek1cecha2)
         for i in range(punktKrzyzowania3, chromosom2cecha2bin.__len__() - 1):
             potomek1cecha2 = list(potomek1cecha2)
             potomek1cecha2[i] = chromosom2cecha2bin[i]
             potomek1cecha2 = "".join(potomek1cecha2)

         if dot1 != dot2:
             if dot1 > dot2:
                 newdot1 = random.randint(dot2, dot1)
             else:
                 newdot1 = random.randint(dot1, dot2)
         else:
             newdot1 = dot1
         if dot3 != dot4:
             if dot3 > dot4:
                 newdot2 = random.randint(dot4, dot3)
             else:
                 newdot2 = random.randint(dot3, dot4)
         else:
             newdot2 = dot2

         potomek1cecha1 = list(potomek1cecha1)
         potomek1cecha1.insert(newdot1, ".")
         potomek1cecha1 = "".join(potomek1cecha1)

         potomek1cecha2 = list(potomek1cecha2)
         potomek1cecha2.insert(newdot2, ".")
         potomek1cecha2 = "".join(potomek1cecha2)

         tmp = individual()
         tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
         tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
         tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
         nowePokolenie.append(tmp)


    if typ=="JJ":
     for x in range(populacja.__len__()):
         if  x==populacja.__len__()-1:  # Krzyzowanie Ostatniego osbonika z populacji z pierwszym
             chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
             chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
             chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha1)
             chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[0].cecha2)
             potomek1cecha1 = chromosom1cecha1bin
             potomek1cecha2 = chromosom1cecha2bin

             dot1 = potomek1cecha1.find(".")
             potomek1cecha1 = list(potomek1cecha1)
             potomek1cecha1.pop(dot1)
             potomek1cecha1 = "".join(potomek1cecha1)
             dot2 = chromosom2cecha1bin.find(".")
             chromosom2cecha1bin = list(chromosom2cecha1bin)
             chromosom2cecha1bin.pop(dot2)
             chromosom2cecha1bin = "".join(chromosom2cecha1bin)
             dot3 = potomek1cecha2.find(".")
             potomek1cecha2 = list(potomek1cecha2)
             potomek1cecha2.pop(dot3)
             potomek1cecha2 = "".join(potomek1cecha2)
             dot4 = chromosom2cecha2bin.find(".")
             chromosom2cecha2bin = list(chromosom2cecha2bin)
             chromosom2cecha2bin.pop(dot4)
             chromosom2cecha2bin = "".join(chromosom2cecha2bin)

             for i in range(chromosom1cecha1bin.__len__()-1):
                 if i%2 == 1:
                     potomek1cecha1 = list(potomek1cecha1)
                     potomek1cecha1[i] = chromosom2cecha1bin[i]
                     potomek1cecha1 = "".join(potomek1cecha1)
             for i in range(chromosom1cecha2bin.__len__()-1):
                 if i % 2 == 1:
                     potomek1cecha2 = list(potomek1cecha2)
                     potomek1cecha2[i] = chromosom2cecha2bin[i]
                     potomek1cecha2 = "".join(potomek1cecha2)

             if dot1 != dot2:
                 if dot1 > dot2:
                     newdot1 = random.randint(dot2, dot1)
                 else:
                     newdot1 = random.randint(dot1, dot2)
             else:
                 newdot1 = dot1
             if dot3 != dot4:
                 if dot3 > dot4:
                     newdot2 = random.randint(dot4, dot3)
                 else:
                     newdot2 = random.randint(dot3, dot4)
             else:
                 newdot2 = dot2

             potomek1cecha1 = list(potomek1cecha1)
             potomek1cecha1.insert(newdot1, ".")
             potomek1cecha1 = "".join(potomek1cecha1)

             potomek1cecha2 = list(potomek1cecha2)
             potomek1cecha2.insert(newdot2, ".")
             potomek1cecha2 = "".join(potomek1cecha2)

             tmp = individual()
             tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
             tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
             tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
             nowePokolenie.append(tmp)
             break
         chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha1)
         chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x].cecha2)
         chromosom2cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x+1].cecha1)
         chromosom2cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, populacja[x+1].cecha2)
         potomek1cecha1 = chromosom1cecha1bin
         potomek1cecha2 = chromosom1cecha2bin

         dot1 = potomek1cecha1.find(".")
         potomek1cecha1 = list(potomek1cecha1)
         potomek1cecha1.pop(dot1)
         potomek1cecha1 = "".join(potomek1cecha1)
         dot2 = chromosom2cecha1bin.find(".")
         chromosom2cecha1bin = list(chromosom2cecha1bin)
         chromosom2cecha1bin.pop(dot2)
         chromosom2cecha1bin = "".join(chromosom2cecha1bin)
         dot3 = potomek1cecha2.find(".")
         potomek1cecha2 = list(potomek1cecha2)
         potomek1cecha2.pop(dot3)
         potomek1cecha2 = "".join(potomek1cecha2)
         dot4 = chromosom2cecha2bin.find(".")
         chromosom2cecha2bin = list(chromosom2cecha2bin)
         chromosom2cecha2bin.pop(dot4)
         chromosom2cecha2bin = "".join(chromosom2cecha2bin)

         for i in range(chromosom2cecha1bin.__len__()-1):
             if i % 2 == 1:
                 potomek1cecha1 = list(potomek1cecha1)
                 potomek1cecha1[i] = chromosom2cecha1bin[i]
                 potomek1cecha1 = "".join(potomek1cecha1)
         for i in range(chromosom2cecha2bin.__len__()-1):
             if i % 2 == 1:
                 potomek1cecha2 = list(potomek1cecha2)
                 potomek1cecha2[i] = chromosom2cecha2bin[i]
                 potomek1cecha2 = "".join(potomek1cecha2)

         if dot1 != dot2:
             if dot1 > dot2:
                 newdot1 = random.randint(dot2, dot1)
             else:
                 newdot1 = random.randint(dot1, dot2)
         else:
             newdot1 = dot1
         if dot3 != dot4:
             if dot3 > dot4:
                 newdot2 = random.randint(dot4, dot3)
             else:
                 newdot2 = random.randint(dot3, dot4)
         else:
             newdot2 = dot2

         potomek1cecha1 = list(potomek1cecha1)
         potomek1cecha1.insert(newdot1, ".")
         potomek1cecha1 = "".join(potomek1cecha1)

         potomek1cecha2 = list(potomek1cecha2)
         potomek1cecha2.insert(newdot2, ".")
         potomek1cecha2 = "".join(potomek1cecha2)

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
            if random.uniform(0,100)<=prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)

                if chromosom1cecha1bin[chromosom1cecha1bin.__len__()-2] == "0":
                    chromosom1cecha1bin = list(chromosom1cecha1bin)
                    chromosom1cecha1bin[chromosom1cecha1bin.__len__()-2] = "1"
                    chromosom1cecha1bin = "".join(chromosom1cecha1bin)
                else:
                    if chromosom1cecha1bin[chromosom1cecha1bin.__len__() - 2] == "1":
                        chromosom1cecha1bin = list(chromosom1cecha1bin)
                        chromosom1cecha1bin[chromosom1cecha1bin.__len__() - 2] = "0"
                        chromosom1cecha1bin = "".join(chromosom1cecha1bin)

                if chromosom1cecha2bin[chromosom1cecha2bin.__len__()-2] == "0":
                    chromosom1cecha2bin = list(chromosom1cecha2bin)
                    chromosom1cecha2bin[chromosom1cecha2bin.__len__() - 2] = "1"
                    chromosom1cecha2bin = "".join(chromosom1cecha2bin)
                else:
                    if chromosom1cecha2bin[chromosom1cecha1bin.__len__() - 2] == "1":
                        chromosom1cecha2bin = list(chromosom1cecha2bin)
                        chromosom1cecha2bin[chromosom1cecha2bin.__len__() - 2] = "0"
                        chromosom1cecha2bin = "".join(chromosom1cecha2bin)

                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(chromosom1cecha1bin)
                tmp.cecha2 = dziesietnaReprezentacja(chromosom1cecha2bin)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)

            else:
                nowePokolenie.append(x)
    if typ == "JP":
        for x in populacja:
            if random.uniform(0, 100) <= prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
                punktMutacji = random.uniform(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                  populacja[x].cecha1).__len__()-1)
                if chromosom1cecha1bin[punktMutacji] == "0":
                    chromosom1cecha1bin = list(chromosom1cecha1bin)
                    chromosom1cecha1bin[punktMutacji] = "1"
                    chromosom1cecha1bin = "".join(chromosom1cecha1bin)
                else:
                   if chromosom1cecha1bin[punktMutacji] == "1":
                    chromosom1cecha1bin = list(chromosom1cecha1bin)
                    chromosom1cecha1bin[punktMutacji] = "0"
                    chromosom1cecha1bin = "".join(chromosom1cecha1bin)
                if chromosom1cecha2bin[punktMutacji] == "0":
                    chromosom1cecha2bin = list(chromosom1cecha2bin)
                    chromosom1cecha2bin[punktMutacji] = "1"
                    chromosom1cecha2bin = "".join(chromosom1cecha2bin)
                else:
                    if chromosom1cecha2bin[punktMutacji] == "1":
                        chromosom1cecha2bin = list(chromosom1cecha2bin)
                        chromosom1cecha2bin[punktMutacji] = "0"
                        chromosom1cecha2bin = "".join(chromosom1cecha2bin)


                tmp = individual()
                tmp.cecha1 = dziesietnaReprezentacja(chromosom1cecha1bin)
                tmp.cecha2 = dziesietnaReprezentacja(chromosom1cecha2bin)
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)

            else:
                nowePokolenie.append(x)
    if typ == "DP":
        for x in populacja:
            if random.uniform(0, 100) <= prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
                punktMutacji = random.uniform(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__()-1)
                punktMutacji2 = random.uniform(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              populacja[x].cecha1).__len__()-1)
                while punktMutacji2 == punktMutacji:
                    punktMutacji2 = random.uniform(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                   populacja[x].cecha1).__len__()-1)
                if chromosom1cecha1bin[punktMutacji] == "0":
                    chromosom1cecha1bin = list(chromosom1cecha1bin)
                    chromosom1cecha1bin[punktMutacji] = "1"
                    chromosom1cecha1bin = "".join(chromosom1cecha1bin)
                else:
                    if chromosom1cecha1bin[punktMutacji] == "1":
                        chromosom1cecha1bin = list(chromosom1cecha1bin)
                        chromosom1cecha1bin[punktMutacji] = "0"
                        chromosom1cecha1bin = "".join(chromosom1cecha1bin)

                if chromosom1cecha2bin[punktMutacji] == "0":
                    chromosom1cecha2bin = list(chromosom1cecha2bin)
                    chromosom1cecha2bin[punktMutacji] = "1"
                    chromosom1cecha2bin = "".join(chromosom1cecha2bin)
                else:
                    if chromosom1cecha2bin[punktMutacji] == "1":
                        chromosom1cecha2bin = list(chromosom1cecha2bin)
                        chromosom1cecha2bin[punktMutacji] = "0"
                        chromosom1cecha2bin = "".join(chromosom1cecha2bin)

                if chromosom1cecha1bin[punktMutacji2] == "0":
                    chromosom1cecha1bin = list(chromosom1cecha1bin)
                    chromosom1cecha1bin[punktMutacji2] = "1"
                    chromosom1cecha1bin = "".join(chromosom1cecha1bin)
                else:
                    if chromosom1cecha1bin[punktMutacji2] == "1":
                        chromosom1cecha1bin = list(chromosom1cecha1bin)
                        chromosom1cecha1bin[punktMutacji2] = "0"
                        chromosom1cecha1bin = "".join(chromosom1cecha1bin)

                if chromosom1cecha2bin[punktMutacji2] == "0":
                    chromosom1cecha2bin = list(chromosom1cecha2bin)
                    chromosom1cecha2bin[punktMutacji2] = "1"
                    chromosom1cecha2bin = "".join(chromosom1cecha2bin)
                else:
                    if chromosom1cecha2bin[punktMutacji2] == "1":
                        chromosom1cecha2bin = list(chromosom1cecha2bin)
                        chromosom1cecha2bin[punktMutacji2] = "0"
                        chromosom1cecha2bin = "".join(chromosom1cecha2bin)

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
        if random.uniform(0, 100) <= prawdobodobienstwo:
            punktinwersji1 = random.randint(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,x.cecha1).__len__() - 4)
            punktinwersji2 = random.randint(punktinwersji1 , binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1).__len__() - 2)

            chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
            chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
            potomek1cecha1 = chromosom1cecha1bin
            potomek1cecha2 = chromosom1cecha2bin
            for i in range(punktinwersji1, punktinwersji2):
                if potomek1cecha1[i] == "0":
                    potomek1cecha1 = list(potomek1cecha1)
                    potomek1cecha1[i] = "1"
                    potomek1cecha1 = "".join(potomek1cecha1)
                else:
                    if potomek1cecha1[i] == "1":
                        potomek1cecha1 = list(potomek1cecha1)
                        potomek1cecha1[i] = "0"
                        potomek1cecha1 = "".join(potomek1cecha1)
            for i in range(punktinwersji1, punktinwersji2):
                if potomek1cecha2[i] == "0":
                    potomek1cecha2 = list(potomek1cecha2)
                    potomek1cecha2[i] = "1"
                    potomek1cecha2 = "".join(potomek1cecha2)
                else:
                    if potomek1cecha2[i] == "1":
                        potomek1cecha2 = list(potomek1cecha2)
                        potomek1cecha2[i] = "0"
                        potomek1cecha2 = "".join(potomek1cecha2)

            tmp = individual()
            tmp.cecha1 = dziesietnaReprezentacja(potomek1cecha1)
            tmp.cecha2 = dziesietnaReprezentacja(potomek1cecha2)
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)
        else:
            nowePokolenie.append(x)

    return nowePokolenie


def licz(ustawienia):
    wynikFinalny=Wynik.objects.create(id=ustawienia.ID_Wyniku)
    populacja=poczatkoweWartosci(ustawienia.wielkoscPopulacji,ustawienia.zakres1,ustawienia.zakres2)
    for i in range(ustawienia.liczbaepok):
        if ustawienia.metodaSelekcji== "SN":
            if(ustawienia.rodzaj_Optymalizacj=="Min"):
                populacja=selekcjaNajelpszychMIN(ustawienia.ileprzechodzi,populacja)
                if random.uniform(0,100)<=ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania,ustawienia.zakres1, ustawienia.zakres2,ustawienia.dokladnosc,populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,ustawienia.prawdobodobienstwoMutowania,ustawienia.zakres1, ustawienia.zakres2,ustawienia.dokladnosc,populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc, populacja)
            else:
                populacja = selekcjaNajelpszychMAX(ustawienia.ileprzechodzi, populacja)
                if random.uniform(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
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
                if random.uniform(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
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
                    if random.uniform(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                        populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                             ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                    populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                     ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                     ustawienia.zakres2, ustawienia.dokladnosc, populacja)
                    populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                      ustawienia.zakres2, ustawienia.dokladnosc, populacja)\

        ustawienia.save()




        sredniwynik = 0
        listawynikow=[]
        for x in populacja:
            sredniwynik += x.wynik
            listawynikow.append(x.wynik)
        sredniWynik=sredniwynik/populacja.__len__()
        wyniki_epoki = Epoka.objects.create(

            czas=timezone.now(),
            iteracja=str(i + 1) + "/" + str(ustawienia.liczbaepok),
            sredniWynik=str(sredniwynik / populacja.__len__()),
            odchylenieStandardowe=statistics.stdev(listawynikow),
            rezultaty=wynikFinalny,
            #wykres= pass
        )
        for x in populacja:
            rezultat=PojedynczaWartoscWyniku.objects.create(
            wartosc = x.wynik,
            x1 = x.cecha1,
            x2 = x.cecha2,
            Wynik=  wyniki_epoki
             )
        ustawienia.nalezy_do=wyniki_epoki
        wyniki_epoki.save()

