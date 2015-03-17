from django.conf import settings

TRIBE_URL = "http://tribe.greenelab.com"

ACCESS_CODE_URL = TRIBE_URL + "/oauth2/authorize/"
ACCESS_TOKEN_URL = TRIBE_URL + "/oauth2/access_token/"

ENTREZ = 'Entrez'

CROSSREF_DB = '&xrdb=' + getattr(settings, 'TRIBE_CROSSREF_DB', ENTREZ)
CROSSREF = getattr(settings, 'TRIBE_CROSSREF_DB', ENTREZ)

TRIBE_ID = getattr(settings, 'TRIBE_ID', '')
TRIBE_SECRET= getattr(settings, 'TRIBE_SECRET', '')

