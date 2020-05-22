from django.db import models
import math

# Create your models here.

class Gen(models.Model):
    allel = models.FloatField()
    locus = models.IntegerField()


class Chromosom(models.Model):
    gen = models.ForeignKey(Gen,on_delete=models.CASCADE)


class Individual(models.Model):
    individual = models.OneToOneField(Chromosom, on_delete=models.CASCADE)
    solution = models.FloatField()
    epoch = models.IntegerField()


class Population(models.Model):
    population = models.ForeignKey(Individual, on_delete=models.CASCADE)


class PojedynczaWartoscWyniku(models.Model):
    wartosc=models.FloatField()
    x1=models.FloatField()
    x2=models.FloatField()

class Wynik(models.Model):
    czas=models.TimeField()
    wyniki=models.ManyToManyField(PojedynczaWartoscWyniku)
    sredniWynik = models.FloatField()
    odchylenieStandardowe = models.FloatField()
    iteracja = models.IntegerField()

class Ustawienia(models.Model):
    zakres1=models.FloatField()
    zakres2 = models.FloatField()
    dokladnosc = models.IntegerField()
    wielkoscPopulacji = models.IntegerField()
    liczbaepok = models.IntegerField()
    metodaSelekcji=models.TextField()
    implementacjaKrzyzowania=models.TextField()
    prawdobodobienstwoKrzyzowania = models.IntegerField()
    implementacjaMutowania = models.TextField()
    prawdobodobienstwoMutowania = models.IntegerField()
    prawdobodobienstwoinwersji = models.IntegerField()
    ileprzechodzi = models.IntegerField()
    rodzaj_Optymalizacj=models.TextField()
