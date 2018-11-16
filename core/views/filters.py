from datetime import date
from django.db.models import Q
from django.forms import CheckboxInput
import django_filters
from dal import autocomplete
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                      Profilo, Prestito)


class LibroFilter(django_filters.FilterSet):
    isbn = django_filters.CharFilter(lookup_expr='iexact')
    titolo = django_filters.CharFilter(
        label="Titolo",
        lookup_expr='icontains',
    )
    autori = django_filters.ModelMultipleChoiceFilter(
        label='Autori',
        field_name='autori',
        queryset= Autore.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='autore_dal',),
    )
    editore = django_filters.ModelChoiceFilter(
        label='Editore',
        field_name='editore',
        required=False,
        queryset= Editore.objects.all(),
        widget=autocomplete.ModelSelect2(url='editore_dal',),
    )
    collana = django_filters.ModelChoiceFilter(
        label='Collana',
        field_name='collana',
        queryset= Collana.objects.all(),
        widget=autocomplete.ModelSelect2(url='collana_dal', forward=('editore',)),
    )
    genere = django_filters.ModelChoiceFilter(
        label='Genere',
        field_name='genere',
        queryset= Genere.objects.all(),
        widget=autocomplete.ModelSelect2(url='genere_dal',),
    )

    class Meta:
        model = Libro
        fields = ['isbn', 'titolo', 'autori', 'editore',
                  'genere', 'collana']


class PrestitoFilter(django_filters.FilterSet):
    stato = django_filters.ChoiceFilter(
        choices=Prestito.STATI_PRESTITO,
        label="Stato prestito"
    )
    libro = django_filters.ModelChoiceFilter(
        label="Libro",
        queryset=Libro.objects.all()
    )
    scaduto = django_filters.BooleanFilter(
        label='Scaduto',
        field_name='data_scadenza',
        widget=CheckboxInput(),
        method="cerca_prestito_scaduto"
    )

    class Meta:
        model = Prestito
        fields = ['profilo']

    def cerca_prestito_scaduto(self, queryset, name, value):
        if value:
            return queryset.filter(data_scadenza__lte=date.today())
        else:
            return queryset
