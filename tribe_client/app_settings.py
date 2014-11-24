from django.conf import settings

TRIBE_URL = "http://tribe.dartmouth.edu"

ENTREZ = 'Entrez'

CROSSREF_DB = '&xrdb=' + getattr(settings, 'TRIBE_CROSSREF_DB', ENTREZ)

TRIBE_ID = getattr(settings, 'TRIBE_ID', '')
TRIBE_SECRET= getattr(settings, 'TRIBE_SECRET', '')

