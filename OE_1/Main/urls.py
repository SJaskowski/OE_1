from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import MainView,WynikDzialania,Epoka,DetaleEpoki

app_name="Main"
urlpatterns = [
    path('',MainView.as_view(),name="main"),
    path('wynik/<id>',WynikDzialania.as_view(),name="wynik"),
    path('Epoka/<pk>',DetaleEpoki.as_view(),name='Epoka'),

]