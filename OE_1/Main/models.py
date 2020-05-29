from django.db import models
from django.shortcuts import reverse
import math


# Create your models here.

class Wynik(models.Model):
    nazwa=models.TextField(null=True,blank=True)

class Ustawienia(models.Model):
    zakres1 = models.FloatField()
    zakres2 = models.FloatField()
    dokladnosc = models.IntegerField()
    wielkoscPopulacji = models.IntegerField()
    liczbaepok = models.IntegerField()
    metodaSelekcji = models.TextField()
    implementacjaKrzyzowania = models.TextField()
    prawdobodobienstwoKrzyzowania = models.IntegerField()
    implementacjaMutowania = models.TextField()
    prawdobodobienstwoMutowania = models.IntegerField()
    prawdobodobienstwoinwersji = models.IntegerField()
    ileprzechodzi = models.IntegerField()
    rodzaj_Optymalizacj = models.TextField()
    wielkosc_turnieju=models.IntegerField(blank=True)
    elita=models.IntegerField(blank=True)
  #  nalezy_do=models.ForeignKey(Epoka,on_delete=models.CASCADE,blank=True,null=True)
    ID_Wyniku=models.TextField()

class Epoka(models.Model):

    czas = models.TextField(blank=True, null=True)
    rezultaty = models.ForeignKey(Wynik, blank=True,on_delete=models.CASCADE)
    sredniWynik = models.TextField(blank=True, default="Brak danych")
    odchylenieStandardowe = models.DecimalField(null=True,blank=True,max_digits=30,decimal_places=3)
    iteracja = models.TextField(blank=True, default="Brak danych")
    #wykres = models.ImageField(blank=True)
    ustawienia = models.ForeignKey(Ustawienia, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("Main:Epoka",kwargs={
            'pk':self.id
        })


    def __str__(self):
        return self.iteracja

class PojedynczaWartoscWyniku(models.Model):
    # wyn_id=models.AutoField(primary_key=True,blank=True)
    wartosc = models.FloatField()
    x1 = models.FloatField()
    x2 = models.FloatField()
    Wynik=models.ForeignKey(Epoka,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.wartosc)





