from django import forms

metoda_Selekcji = (
    ('SN', 'Selekcja Najlepszych'),
    ('SR', 'Selekcja Kołem ruletki'),
    ('ST', 'Selekcja Turniejowa')
)
implementacja_Krzyzowania = (
    ('JP', 'Krzyżowanie jednopunkotwe'),
    ('DP', 'Krzyżowanie dwupunktowe'),
    ('TP', 'Krzyżowanie trzyupunktowe'),
    ('JJ', 'Krzyżowanie jednorodne'),

)
implementacja_Mutacji = (
    ('MB', 'Mutacja Brzegowa'),
    ('JP', 'Mutacja jednopuktowa'),
    ('DP', 'Mutacja dwupunktowa'),

)
rodzaj_Optymalizacj = (
    ('Min', 'Minimalne'),
    ('Max', 'Maksymalne'),

)


class FormularzPoczatkowy(forms.Form):
    zakres1 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Minimalna wartość zmiennej",'size':'25'}))
    zakres2 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Maksymalna wartość zmiennej",'size':'25'}))
    dokladnosc_reprezentacji_chromsomu = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Dokładność reprezentacji chromosomu",'size':'32'}))
    wielkosc_populacji = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Wielkość populacji",'size':'25'}))
    liczba_epok = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Liczba epok",'size':'25'}))
    rodzaj_Optymalizacj = forms.ChoiceField(choices=rodzaj_Optymalizacj, widget=forms.RadioSelect)
    metoda_Selekcji = forms.ChoiceField(choices=metoda_Selekcji, widget=forms.RadioSelect)
    implementacja_Krzyzowania = forms.ChoiceField(choices=implementacja_Krzyzowania, widget=forms.RadioSelect)
    prawdopodbienstwo_Krzyzowania = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Ile % szansy na wystąpienie krzyżowania",'size':'34'}))
    implementacja_MutacjiBrzegowej = forms.ChoiceField(choices=implementacja_Mutacji, widget=forms.RadioSelect)
    prawdopodbienstwo_MutacjiBrzegowej = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Ile % szansy na wystąpienie mutacji",'size':'30'}))
    prawdopodbienstwo_OperatoraInwersji = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Ile % szansy na wystąpienie inwersji",'size':'30'}))
    ile_Przechodzi = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"  Domyślnie 30% ",'size':'12'}),required=False)
    wielkosc_turnieju=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Domyślnie 3"}),required=False)
    elita=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Strategia elitarna, ilu osobników przechodzi",'size':'37'}))
   # ID_Wyniku = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"ID_Wyniku"}))