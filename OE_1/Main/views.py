from Genetic.selection import tournamentSelect,getRouletteWheel,rouletteWheelSelect,Individual
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,DetailView,ListView
from .forms import FormularzPoczatkowy
from  .models import Epoka,PojedynczaWartoscWyniku,Ustawienia,Wynik
from django.contrib import messages
from django.utils import timezone
import statistics,math,random
import heapq



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
                implementacja_MutacjiBrzegowej = formularz.cleaned_data.get('implementacja_MutacjiBrzegowej')
                prawdopodbienstwo_MutacjiBrzegowej = formularz.cleaned_data.get('prawdopodbienstwo_MutacjiBrzegowej')
                prawdopodbienstwo_OperatoraInwersji = formularz.cleaned_data.get('prawdopodbienstwo_OperatoraInwersji')
                ile_Przechodzi = formularz.cleaned_data.get('ile_Przechodzi')
                if ile_Przechodzi is None:
                    ile_Przechodzi=30

                rodzaj_Optymalizacj=formularz.cleaned_data.get('rodzaj_Optymalizacj')
                wielkosc_turnieju=formularz.cleaned_data.get('wielkosc_turnieju')
                elita=formularz.cleaned_data.get('elita')
                if wielkosc_turnieju is None:
                    wielkosc_turnieju=3
                if dokladnosc_reprezentacji_chromsomu < 3:
                    dokladnosc_reprezentacji_chromsomu=6
                if wielkosc_populacji-elita <= round(wielkosc_populacji*(ile_Przechodzi/100)):
                    elita=elita-round(wielkosc_populacji*(ile_Przechodzi/100))
               # ID_Wyniku= formularz.cleaned_data.get('ID_Wyniku')
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
                    wielkosc_turnieju=wielkosc_turnieju,
                    elita=elita
                    #

                )

                return redirect('Main:wynik',licz(ustawienia))
        else:
            messages.warning(self.request, "Błędnie uzupełniony formularz")
            return redirect("Main:main")



class WynikDzialania(ListView):
    model = Epoka

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        id_wyniku = self.request.path.rsplit("/")
        id_wyniku=id_wyniku[-1]
        Wyniki = Wynik.objects.filter(id=id_wyniku)
        ustawienia= Wyniki[0].epoka_set.all()[0]
        lista_srednich=[]
        lista_odchylen = []
        iteracja= []
        czas=0
        for x in Wyniki[0].epoka_set.all():
            lista_srednich.append(float(x.sredniWynik))
            lista_odchylen.append(str(x.odchylenieStandardowe))
            czas+=float(x.czas)
            tmp=x.iteracja.rsplit("/")
            tmp=tmp[0]
            iteracja.append(tmp)

        if(ustawienia.ustawienia.rodzaj_Optymalizacj=='Min'):
            maks=min(lista_srednich)
            najelpsza_epoka=lista_srednich.index(maks)+1
        else:
            maks = max(lista_srednich)
            najelpsza_epoka = lista_srednich.index(maks) + 1

        context= {"srednie": lista_srednich,
                   "odchylenie": lista_odchylen,
                   "Epoka": Wyniki[0].epoka_set.all(),
                   "iteracja":iteracja,
                   "czas":czas,
                   "ustawienia":ustawienia,
                    "maks":maks,
                    "najelpsza_epoka":najelpsza_epoka
                   }


        return context
    template_name = "Wynik.html"

class DetaleEpoki(DetailView):
        model = Epoka

        def get_context_data(self, **kwargs):
            context = super().get_context_data()
            lista_x = []
            lista_y = []
            lista_z = []


            for x in self.object.pojedynczawartoscwyniku_set.all():
                lista_x.append(x.x1)
                lista_y.append(x.x2)
                lista_z.append(x.wartosc)
            if self.object.ustawienia.rodzaj_Optymalizacj == "Min":
                najelpszyWyniki=self.object.pojedynczawartoscwyniku_set.all()[lista_z.index(min(lista_z))]
            else:
                najelpszyWyniki = self.object.pojedynczawartoscwyniku_set.all()[lista_z.index(max(lista_z))]
            context ['lista_x'] = lista_x
            context['lista_y'] =  lista_y
            context['lista_z'] =  lista_z
            context['zakres1'] = self.object.ustawienia.zakres1
            context['zakres2'] = self.object.ustawienia.zakres2
            context['min'] = min(lista_z)
            context['max'] = max(lista_z)
            context['najlepszy']=najelpszyWyniki

            return context

        template_name = "Epoka_detale.html"



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


def selekcjaNajelpszychMAX(ustawienia,populacja=[]):
    licznik=round((ustawienia.ileprzechodzi/100)*populacja.__len__())
    najelpsze=[]
    lista_wynikow=[]
    Populacja_elity=[]
    for x in populacja:
        lista_wynikow.append(x.wynik)
    elita=heapq.nlargest(ustawienia.elita,lista_wynikow)
    for i in elita:
        x=populacja[elita.index(i)]
        Populacja_elity.append(x)
        lista_wynikow.remove(x.wynik)
        populacja.remove(x)
    tmp = heapq.nlargest(licznik, lista_wynikow)
    for i in tmp:
        najelpsze.append(populacja[tmp.index(i)])

    for i in range(najelpsze.__len__(),populacja.__len__()):
        najelpsze.append(najelpsze[random.randint(0,najelpsze.__len__()-1)])


    return najelpsze,Populacja_elity

def selekcjaNajelpszychMIN(ustawienia, populacja=[]):
    licznik = round((ustawienia.ileprzechodzi / 100) * populacja.__len__())
    najelpsze = []
    lista_wynikow = []
    Populacja_elity = []
    for x in populacja:
        lista_wynikow.append(x.wynik)
    elita = heapq.nsmallest(ustawienia.elita, lista_wynikow)
    for i in elita:
        x = populacja[elita.index(i)]
        Populacja_elity.append(x)
        lista_wynikow.remove(x.wynik)
        populacja.remove(x)
    tmp = heapq.nsmallest(licznik, lista_wynikow)
    for i in tmp:
        najelpsze.append(populacja[tmp.index(i)])
    for i in range(najelpsze.__len__(), populacja.__len__()):
        najelpsze.append(najelpsze[random.randint(0, najelpsze.__len__() - 1)])

    return najelpsze,Populacja_elity

#todo check strategia elitarna

def selecjaTurniejowa(ustawienia, populacja=[]):
    answer = []
    lista_wynikow = []
    Populacja_elity = []
    if ustawienia.rodzaj_Optymalizacj=='Min':
        #elita

        for x in populacja:
            lista_wynikow.append(x.wynik)
        elita = heapq.nsmallest(ustawienia.elita, lista_wynikow)
        for i in elita:
            x = populacja[elita.index(i)]
            Populacja_elity.append(x)
            populacja.remove(x)
        lista_wynikow=[]
        # elita
        for x in populacja:
            lista_wynikow.append(x.wynik)
        while len(answer) < ustawienia.wielkoscPopulacji:
            tmp = random.sample(populacja, ustawienia.wielkosc_turnieju)
            best = max(lista_wynikow)
            for i in tmp:
                if i.wynik < best:
                    best = i.wynik
            answer.append(populacja[lista_wynikow.index(best)])
    else:
        # elita

        for x in populacja:
            lista_wynikow.append(x.wynik)
        elita = heapq.nlargest(ustawienia.elita, lista_wynikow)
        for i in elita:
            x = populacja[elita.index(i)]
            Populacja_elity.append(x)
            populacja.remove(x)
        lista_wynikow = []
        # elita
        for x in populacja:
            lista_wynikow.append(x.wynik)
        while len(answer) < ustawienia.wielkoscPopulacji:
            tmp=random.sample(populacja, ustawienia.wielkosc_turnieju)
            best=0
            for i in tmp:
                if i.wynik >best:
                    best=i.wynik
            answer.append(populacja[lista_wynikow.index(best)])
    return answer,Populacja_elity


def selekcjaKolemRuletki(ustawienia,populacja=[]):
    score={}
    lista_wynikow=[]
    Populacja_elity=[]
    najlepsi=[]
    if ustawienia.rodzaj_Optymalizacj=="Max":
        # elita

        for x in populacja:
            lista_wynikow.append(x.wynik)
        elita = heapq.nlargest(ustawienia.elita, lista_wynikow)
        for i in elita:
            x = populacja[elita.index(i)]
            Populacja_elity.append(x)
            populacja.remove(x)
            lista_wynikow = []
        # elita
        for indiv in populacja:
            score.update({indiv:indiv.wynik})
        for x in range(0,populacja.__len__()):
         najlepsi.append(rouletteWheelSelect(getRouletteWheel(populacja,score)))
    else:
        if ustawienia.rodzaj_Optymalizacj == "Min":
            # elita

            for x in populacja:
                lista_wynikow.append(x.wynik)
            elita = heapq.nsmallest(ustawienia.elita, lista_wynikow)
            for i in elita:
                x = populacja[elita.index(i)]
                Populacja_elity.append(x)
                populacja.remove(x)
                lista_wynikow=[]
            # elita
            for indiv in populacja:
                score.update({indiv: 1/indiv.wynik})
            for x in range(0, populacja.__len__()):
                najlepsi.append(rouletteWheelSelect(getRouletteWheel(populacja, score)))
    return najlepsi,Populacja_elity


def implementacjaKrzyzowania(typ, zakres1, zakres2, dokladnosc,elita, populacja=[]):
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
                x=dziesietnaReprezentacja(potomek1cecha1)
                y=dziesietnaReprezentacja(potomek1cecha2)
                if x<zakres1 or x>zakres2:
                  if x-zakres1 < x-zakres2:
                      x=zakres1
                  else:
                      x=zakres2
                if y<zakres1 or y>zakres2:
                  if y-zakres1 < y-zakres2:
                      y=zakres1
                  else:
                      y=zakres2
                tmp.cecha1 = x
                tmp.cecha2 = y
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
            x = dziesietnaReprezentacja(potomek1cecha1)
            y = dziesietnaReprezentacja(potomek1cecha2)
            if x < zakres1 or x > zakres2:
                if x - zakres1 < x - zakres2:
                    x = zakres1
                else:
                    x = zakres2
            if y < zakres1 or y > zakres2:
                if y - zakres1 < y - zakres2:
                    y = zakres1
                else:
                    y = zakres2
            tmp.cecha1 = x
            tmp.cecha2 = y
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
                x = dziesietnaReprezentacja(potomek1cecha1)
                y = dziesietnaReprezentacja(potomek1cecha2)
                if x < zakres1 or x > zakres2:
                    if x - zakres1 < x - zakres2:
                        x = zakres1
                    else:
                        x = zakres2
                if y < zakres1 or y > zakres2:
                    if y - zakres1 < y - zakres2:
                        y = zakres1
                    else:
                        y = zakres2
                tmp.cecha1 = x
                tmp.cecha2 = y
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
            x = dziesietnaReprezentacja(potomek1cecha1)
            y = dziesietnaReprezentacja(potomek1cecha2)
            if x < zakres1 or x > zakres2:
                if x - zakres1 < x - zakres2:
                    x = zakres1
                else:
                    x = zakres2
            if y < zakres1 or y > zakres2:
                if y - zakres1 < y - zakres2:
                    y = zakres1
                else:
                    y = zakres2
            tmp.cecha1 = x
            tmp.cecha2 = y
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
             x = dziesietnaReprezentacja(potomek1cecha1)
             y = dziesietnaReprezentacja(potomek1cecha2)
             if x < zakres1 or x > zakres2:
                 if x - zakres1 < x - zakres2:
                     x = zakres1
                 else:
                     x = zakres2
             if y < zakres1 or y > zakres2:
                 if y - zakres1 < y - zakres2:
                     y = zakres1
                 else:
                     y = zakres2
             tmp.cecha1 = x
             tmp.cecha2 = y
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
         x = dziesietnaReprezentacja(potomek1cecha1)
         y = dziesietnaReprezentacja(potomek1cecha2)
         if x < zakres1 or x > zakres2:
             if x - zakres1 < x - zakres2:
                 x = zakres1
             else:
                 x = zakres2
         if y < zakres1 or y > zakres2:
             if y - zakres1 < y - zakres2:
                 y = zakres1
             else:
                 y = zakres2
         tmp.cecha1 = x
         tmp.cecha2 = y
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
             x = dziesietnaReprezentacja(potomek1cecha1)
             y = dziesietnaReprezentacja(potomek1cecha2)
             if x < zakres1 or x > zakres2:
                 if x - zakres1 < x - zakres2:
                     x = zakres1
                 else:
                     x = zakres2
             if y < zakres1 or y > zakres2:
                 if y - zakres1 < y - zakres2:
                     y = zakres1
                 else:
                     y = zakres2
             tmp.cecha1 = x
             tmp.cecha2 = y
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
         x = dziesietnaReprezentacja(potomek1cecha1)
         y = dziesietnaReprezentacja(potomek1cecha2)
         if x < zakres1 or x > zakres2:
             if x - zakres1 < x - zakres2:
                 x = zakres1
             else:
                 x = zakres2
         if y < zakres1 or y > zakres2:
             if y - zakres1 < y - zakres2:
                 y = zakres1
             else:
                 y = zakres2
         tmp.cecha1 = x
         tmp.cecha2 = y
         tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
         nowePokolenie.append(tmp)
    return nowePokolenie


def implementacjaMutacji(typ,prawdobodobienstwo, zakres1, zakres2, dokladnosc,elita,populacja=[]):
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
                x = dziesietnaReprezentacja(chromosom1cecha1bin)
                y = dziesietnaReprezentacja(chromosom1cecha2bin)
                if x < zakres1 or x > zakres2:
                    if x - zakres1 < x - zakres2:
                        x = zakres1
                    else:
                        x = zakres2
                if y < zakres1 or y > zakres2:
                    if y - zakres1 < y - zakres2:
                        y = zakres1
                    else:
                        y = zakres2
                tmp.cecha1 = x
                tmp.cecha2 = y
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)

            else:
                nowePokolenie.append(x)
    if typ == "JP":
        for x in populacja:
            if random.uniform(0, 100) <= prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
                punktMutacji = random.randint(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                  x.cecha1).__len__()-1)
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
                x = dziesietnaReprezentacja(chromosom1cecha1bin)
                y = dziesietnaReprezentacja(chromosom1cecha2bin)
                if x < zakres1 or x > zakres2:
                    if x - zakres1 < x - zakres2:
                        x = zakres1
                    else:
                        x = zakres2
                if y < zakres1 or y > zakres2:
                    if y - zakres1 < y - zakres2:
                        y = zakres1
                    else:
                        y = zakres2
                tmp.cecha1 = x
                tmp.cecha2 = y
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)

            else:
                nowePokolenie.append(x)
    if typ == "DP":
        for x in populacja:
            if random.uniform(0, 100) <= prawdobodobienstwo:
                chromosom1cecha1bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha1)
                chromosom1cecha2bin = binarnaReprezentacja(zakres1, zakres2, dokladnosc, x.cecha2)
                punktMutacji = random.randint(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              x.cecha1).__len__()-1)
                punktMutacji2 = random.randint(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                              x.cecha1).__len__()-1)
                while punktMutacji2 == punktMutacji:
                    punktMutacji2 = random.randint(0, binarnaReprezentacja(zakres1, zakres2, dokladnosc,
                                                                   x.cecha1).__len__()-1)
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
                x = dziesietnaReprezentacja(chromosom1cecha1bin)
                y = dziesietnaReprezentacja(chromosom1cecha2bin)
                if x < zakres1 or x > zakres2:
                    if x - zakres1 < x - zakres2:
                        x = zakres1
                    else:
                        x = zakres2
                if y < zakres1 or y > zakres2:
                    if y - zakres1 < y - zakres2:
                        y = zakres1
                    else:
                        y = zakres2
                tmp.cecha1 = x
                tmp.cecha2 = y
                tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
                nowePokolenie.append(tmp)
            else:
                nowePokolenie.append(x)
    return nowePokolenie


def implementacjaInwersji(prawdobodobienstwo, zakres1, zakres2, dokladnosc,elita,populacja=[]):
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
            x = dziesietnaReprezentacja(potomek1cecha1)
            y = dziesietnaReprezentacja(potomek1cecha2)
            if x < zakres1 or x > zakres2:
                if x - zakres1 < x - zakres2:
                    x = zakres1
                else:
                    x = zakres2
            if y < zakres1 or y > zakres2:
                if y - zakres1 < y - zakres2:
                    y = zakres1
                else:
                    y = zakres2
            tmp.cecha1 = x
            tmp.cecha2 = y
            tmp.wynik = bealeFunction(tmp.cecha1, tmp.cecha2)
            nowePokolenie.append(tmp)
        else:
            nowePokolenie.append(x)

    return nowePokolenie


def licz(ustawienia):

    wynikFinalny=Wynik.objects.create()
    populacja=poczatkoweWartosci(ustawienia.wielkoscPopulacji,ustawienia.zakres1,ustawienia.zakres2)
    for i in range(ustawienia.liczbaepok):
        startime = timezone.now()
        if ustawienia.metodaSelekcji== "SN":
            if(ustawienia.rodzaj_Optymalizacj=="Min"):
                populacja,elita=selekcjaNajelpszychMIN(ustawienia,populacja)
                if random.uniform(0,100)<=ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania,ustawienia.zakres1, ustawienia.zakres2,ustawienia.dokladnosc,ustawienia.elita,populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,ustawienia.prawdobodobienstwoMutowania,ustawienia.zakres1, ustawienia.zakres2,ustawienia.dokladnosc,ustawienia.elita,populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja=populacja+elita
            else:
                populacja,elita = selekcjaNajelpszychMAX(ustawienia, populacja)
                if random.uniform(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                         ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                 ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                  ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja=populacja+elita
        else:
            if ustawienia.metodaSelekcji== "SR":
                populacja,elita = selekcjaKolemRuletki(ustawienia,populacja)
                if random.uniform(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                    populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                         ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                 ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                 ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                  ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                populacja=populacja+elita
            else:
                if ustawienia.metodaSelekcji == "ST":
                    populacja,elita = selecjaTurniejowa(ustawienia, populacja)
                    if random.uniform(0, 100) <= ustawienia.prawdobodobienstwoKrzyzowania:
                        populacja = implementacjaKrzyzowania(ustawienia.implementacjaKrzyzowania, ustawienia.zakres1,
                                                             ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                    populacja = implementacjaMutacji(ustawienia.implementacjaMutowania,
                                                     ustawienia.prawdobodobienstwoMutowania, ustawienia.zakres1,
                                                     ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                    populacja = implementacjaInwersji(ustawienia.prawdobodobienstwoinwersji, ustawienia.zakres1,
                                                      ustawienia.zakres2, ustawienia.dokladnosc,ustawienia.elita, populacja)
                    populacja=populacja+elita






        sredniwynik = 0
        listawynikow=[]
        listax=[]
        listay=[]
        listaz=[]

        for x in populacja:
            sredniwynik += x.wynik
            listawynikow.append(x.wynik)
            listax.append(x.cecha1)
            listay.append(x.cecha2)
            listaz.append(x.wynik)



        ustawienia.save()
        czas=timezone.now()-startime
        czas= str(czas).split(".")
        sekundy=str(czas[0].rsplit(":")[-1])
        setnes=czas[-1]
        czas=sekundy+"."+setnes
        wyniki_epoki = Epoka.objects.create(

            czas=czas,
            iteracja=str(i + 1) + "/" + str(ustawienia.liczbaepok),
            sredniWynik=str(sredniwynik / populacja.__len__()),
            odchylenieStandardowe=statistics.stdev(listawynikow),
            rezultaty=wynikFinalny,
            ustawienia=ustawienia
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

    return wynikFinalny.id