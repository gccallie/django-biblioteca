from django.conf import settings

DURATA_PRESTITO = getattr(
    settings,
    'BIBLIOTECA_DURATA_PRESTITO',
    30
)

MAX_LIBRI_INPRESTITO = getattr(
    settings,
    'BIBLIOTECA_MAX_LIBRI_INPRESTITO',
    4
)