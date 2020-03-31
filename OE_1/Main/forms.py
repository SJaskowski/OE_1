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
implementacja_MutacjiBrzegowej = (
    ('JP', 'Mutacja jednopuktowa'),
    ('DP', 'Mutacja dwupunktowa'),

)


class FormularzPoczatkowy(forms.Form):
    zakres1 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Zakres funkcji z lewej strony"}))
    zakres2 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Zakres funkcji z Prawej strony"}))
    dokladnosc_reprezentacji_chromsomu = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"dokladnosc_reprezentacji_chromsomu"}))
    wielkosc_populacji = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"wielkosc_populacji"}))
    liczba_epok = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"liczba_epok"}))
    metoda_Selekcji = forms.ChoiceField(choices=metoda_Selekcji, widget=forms.RadioSelect)
    implementacja_Krzyzowania = forms.ChoiceField(choices=implementacja_Krzyzowania, widget=forms.RadioSelect)
    prawdopodbienstwo_Krzyzowania = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"prawdopodbienstwo_Krzyzowania"}))
    implementacja_MutacjiBrzegowej = forms.ChoiceField(choices=implementacja_MutacjiBrzegowej, widget=forms.RadioSelect)
    prawdopodbienstwo_MutacjiBrzegowej = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"prawdopodbienstwo_MutacjiBrzegowej"}))
    prawdopodbienstwo_OperatoraInwersji = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"prawdopodbienstwo_OperatoraInwersji"}))
    ile_Przechodzi = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':"Ile % najepszych prezchodzi do następnej epoki"}))
