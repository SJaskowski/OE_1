from django.db import models


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
