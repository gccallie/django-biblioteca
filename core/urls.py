from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    # Libri
    path('elenco-libri/', views.ElencoLibriView.as_view(),
        name='elenco_libri'),
    path('elenco-libri/<int:pk>/', views.DettaglioLibroView.as_view(),
        name='dettaglio_libro'),
    path('elenco-libri/aggiungi-libro/', views.AggiungiLibroView.as_view(),
        name='aggiungi_libro'),
    path('elenco-libri/<int:pk>/modifica-libro/', views.ModificaLibroView.as_view(),
        name='modifica_libro'),
    # Autori
    path('elenco-autori/', views.ElencoAutoriView.as_view(),
        name='elenco_autori'),
    path('elenco-autori/aggiungi-autore/', views.AggiungiAutoreView.as_view(),
        name='aggiungi_autore'),
    path('elenco-autori/<int:pk>/modifica-autore/', views.ModificaAutoreView.as_view(),
        name='modifica_autore'),
    # Generi - Sottogeneri
    path('elenco-generi-sottogeneri/', views.ElencoGeneriSottogeneriView.as_view(),
        name='elenco_generi_sottogeneri'),
    path('elenco-generi-sottogeneri/aggiungi-genere/', views.AggiungiGenereView.as_view(),
        name='aggiungi_genere'),
    path('elenco-generi-sottogeneri/<int:pk>/modifica-genere/', views.ModificaGenereView.as_view(),
        name='modifica_genere'),
    path('elenco-generi-sottogeneri/aggiungi-sottogenere/', views.AggiungiSottoGenereView.as_view(),
        name='aggiungi_sottogenere'),
    path('elenco-generi-sottogeneri/<int:pk>/modifica-sottogenere/', views.ModificaSottoGenereView.as_view(),
        name='modifica_sottogenere'),
    # Editori - Collane
    path('elenco-editori-collane/', views.ElencoEditoriCollaneView.as_view(),
        name='elenco_editori_collane'),
    path('elenco-editori-collane/aggiungi-editore/', views.AggiungiEditoreView.as_view(),
        name='aggiungi_editore'),
    path('elenco-editori-collane/<int:pk>/modifica-editore/', views.ModificaEditoreView.as_view(),
        name='modifica_editore'),
    path('elenco-editori-collane/aggiungi-collana/', views.AggiungiCollanaView.as_view(),
        name='aggiungi_collana'),
    path('elenco-editori-collane/<int:pk>/modifica-collana/', views.ModificaCollanaView.as_view(),
        name='modifica_collana'),

]
