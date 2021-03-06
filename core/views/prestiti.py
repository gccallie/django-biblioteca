from datetime import date
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        LoginRequiredMixin)
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  FormView)
from ..settings import MAX_LIBRI_INPRESTITO
from ..models import (Libro, Profilo, Prestito)
from ..forms import (ProfiloForm, PrestitoForm, SegnalazioneForm)
from .mixins import FilteredQuerysetMixin
from .filters import PrestitoFilter


class ElencoPrestitiView(PermissionRequiredMixin, LoginRequiredMixin, FilteredQuerysetMixin, ListView):
    permission_required = 'core.view_prestito'
    template_name = 'core/elenco_prestiti.html'
    model = Prestito
    filter_class = PrestitoFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Prestiti'
        context['sottotitolo'] = '({})'.format(self.get_queryset().count())
        return context


class DettaglioPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.view_dettaglio_prestito'
    template_name = 'core/dettaglio_prestito.html'
    model = Prestito
    context_object_name = 'prestito'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '"{}"'.format(self.object.libro.get_titolo_autori_display())
        context['sottotitolo'] = '({})'.format(self.object.get_stato_display())
        return context


class PrestitoUpdateProfiloView(CreateView):
    template_name = 'core/prestito_update_profilo.html'
    model = Prestito
    form_class = PrestitoForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        libro = Libro.objects.get(pk=self.kwargs['libro_pk'])
        context['libro'] = libro
        context['titolo'] = 'Richiesta Prestito: "{}"'.format(libro.get_titolo_autori_display())
        context['max_libri_prestito'] = MAX_LIBRI_INPRESTITO
        context['annulla_link'] = reverse('catalogo')
        return context

    def get_success_url(self):
        return reverse('catalogo')

    def form_valid(self, form):
        prestito = form.instance
        try:
            with transaction.atomic():
                libro = Libro.objects.get(pk=self.kwargs['libro_pk'])
                profilo = Profilo.objects.select_for_update(nowait=True).get(pk=prestito.profilo.pk)
                if profilo.tot_richieste >= MAX_LIBRI_INPRESTITO:
                    messages.error(self.request, "E' possibile richiede al massimo {} libri alla volta".format(MAX_LIBRI_INPRESTITO))
                    return HttpResponseRedirect(redirect_to=reverse('catalogo'))
                if profilo.is_sospeso:
                    messages.error(self.request, "ATTENZIONE: questo profilo è sospeso fino al {}".format(profilo.data_fine_sospensione))
                    return HttpResponseRedirect(redirect_to=reverse('catalogo'))
                profilo.tot_richieste += 1
                profilo.save()
                prestito.libro = libro
                prestito.stato = Prestito.RICHIESTO
                prestito.save()
                messages.success(self.request, "Richiesta prestito registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return super().form_valid(form)


class PrestitoCreateProfiloView(FormView):
    template_name = 'core/prestito_create_profilo.html'
    form_class = ProfiloForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        libro = Libro.objects.filter(pk=self.kwargs['libro_pk']).first()
        context['titolo'] = 'Richiesta Prestito: "{}"'.format(libro.get_titolo_autori_display())
        context['annulla_link'] = reverse('catalogo')
        return context

    def get_success_url(self):
        return reverse('catalogo')

    def form_valid(self, form):
        profilo = form.instance
        try:
            with transaction.atomic():
                libro = Libro.objects.get(pk=self.kwargs['libro_pk'])
                profilo.tot_richieste += 1
                profilo.save()
                prestito_dict = {
                    'libro': libro,
                    'profilo': profilo,
                    'stato': Prestito.RICHIESTO
                }
                prestito = Prestito.objects.create(**prestito_dict)
                prestito.save()
                messages.success(self.request, "Richiesta prestito registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return super().form_valid(form)


class ConsegnaLibroPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Prestito

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                prestito = Prestito.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                profilo = Profilo.objects.select_for_update(nowait=True).get(pk=prestito.profilo.pk)
                if prestito.is_incorso():
                    messages.error(self.request, "Questo prestito è già in corso.")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))
                if profilo.tot_libri >= MAX_LIBRI_INPRESTITO:
                    messages.error(self.request, "E' possibile avere in prestito al massimo {} libri alla volta".format(MAX_LIBRI_INPRESTITO))
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))
                if profilo.tot_richieste == 0:
                    messages.error(self.request, "Questo profilo non ha richieste in atto.")
                    return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))
                profilo.tot_libri += 1
                profilo.tot_richieste -= 1
                profilo.save()
                prestito.stato = Prestito.INCORSO
                prestito.data_inizio = date.today()
                prestito.save()
                prestito.data_scadenza = prestito.calc_data_scadenza()
                prestito.save()
                messages.success(self.request, "Consegna libro registrata con successo.")
        except ObjectDoesNotExist:
            messages.error(self.request)
        return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))


class RifiutaRichiestaPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Prestito

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                prestito = Prestito.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                profilo = Profilo.objects.select_for_update(nowait=True).get(pk=prestito.profilo.pk)
                if profilo.tot_richieste == 0:
                    messages.error(self.request, "Questo profilo non ha richieste di prestito")
                    return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))
                profilo.tot_richieste -= 1
                profilo.save()
                prestito.delete()
                messages.success(self.request, "Richiesta prestito rifiutata.")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))


class RestituzioneLibroPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Prestito

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                prestito = Prestito.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                profilo = Profilo.objects.select_for_update(nowait=True).get(pk=prestito.profilo.pk)
                if prestito.is_richiesto():
                    messages.error(self.request, "Questo prestito non è ancora stato consegnato.")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))
                if profilo.tot_libri == 0:
                    messages.error(self.request, "Questo profilo non ha prestiti")
                    return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))

                prestito.stato = Prestito.CONCLUSO
                profilo.tot_libri -= 1
                profilo.save()
                prestito.save()
                messages.success(self.request, "Restituzione libro registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))


class SegnalaProfiloView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.sospendi_profilo'
    template_name = 'core/segnalazione_form.html'
    form_class = SegnalazioneForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        profilo = Profilo.objects.filter(pk=self.kwargs['profilo_pk']).first()
        context['titolo'] = 'Sospensione Prestito: "{}"'.format(profilo)
        context['annulla_link'] = reverse('elenco_prestiti')
        return context

    def get_success_url(self):
        return reverse('elenco_prestiti')

    def form_valid(self, form):
        segnalazione = form.save()
        print(segnalazione)
        try:
            with transaction.atomic():
                profilo = Profilo.objects.select_for_update(nowait=True).get(pk=self.kwargs['profilo_pk'])
                if form.cleaned_data['sospendi']:
                    profilo.data_inizio_sospensione = date.today()
                    profilo.save()
                    profilo.data_fine_sospensione = profilo.calculate_fine_sospensione()
                    messages.success(self.request, "Sospensione profilo avviata con successo")
                #segnalazione = form.save()
                profilo.segnalazioni.add(segnalazione)
                profilo.save()
                messages.success(self.request, "Segnalazione effettuata con successo.")
        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return super().form_valid(form)
