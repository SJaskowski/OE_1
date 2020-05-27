from django import forms

metoda_Selekcji = (
    ('SN', 'Selekcja Najlepszych'),
    ('SR', 'Selkecja kołem ruletki'),
    ('ST', 'Selekcja turniejowa')
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
    ('Min', 'Minimalizacja'),
    ('Max', 'Maksymalizacja'),

)


class FormularzPoczatkowy(forms.Form):
    zakres1 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Zakres funkcji z lewej strony"}))
    zakres2 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Zakres funkcji z Prawej strony"}))
    dokladnosc_reprezentacji_chromsomu = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"dokladnosc_reprezentacji_chromsomu"}))
    wielkosc_populacji = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"wielkosc_populacji"}))
    liczba_epok = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"liczba_epok"}))
    rodzaj_Optymalizacj = forms.ChoiceField(choices=rodzaj_Optymalizacj, widget=forms.RadioSelect)
    metoda_Selekcji = forms.ChoiceField(choices=metoda_Selekcji, widget=forms.RadioSelect)
    implementacja_Krzyzowania = forms.ChoiceField(choices=implementacja_Krzyzowania, widget=forms.RadioSelect)
    prawdopodbienstwo_Krzyzowania = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"prawdopodbienstwo_Krzyzowania"}))
    implementacja_MutacjiBrzegowej = forms.ChoiceField(choices=implementacja_Mutacji, widget=forms.RadioSelect)
    prawdopodbienstwo_MutacjiBrzegowej = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"prawdopodbienstwo_Mutacji"}))
    prawdopodbienstwo_OperatoraInwersji = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"prawdopodbienstwo_OperatoraInwersji"}))
    ile_Przechodzi = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Ile % najepszych prezchodzi do następnej epoki"}))
    ID_Wyniku = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"ID_Wyniku"}))