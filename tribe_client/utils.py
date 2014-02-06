import requests
from app_settings import *
# from genes.models import Gene


def get_access_token(authorization_code):

    parameters = {"client_id": TRIBE_ID, "client_secret": TRIBE_SECRET,  "grant_type": "authorization_code",  "code": authorization_code,  "scope": "read"}
    tribe_connection = requests.post("http://" +  TRIBE_URL +  "/oauth2/access_token", data=parameters)
    result = tribe_connection.json()
    print(result)
    access_token = result['access_token']
    return access_token

def retrieve_public_genesets(options={}):
    genesets_url = 'http://'+ TRIBE_URL + '/api/v1/geneset/?format=json&organism__slug=homo-sapiens'

    for opt_key,opt in options.iteritems():
        genesets_url += '&'+opt_key+'='+opt

    try:
        tribe_connection = requests.get(genesets_url)
        result = tribe_connection.json()
        genesets = result['objects']
        return genesets

    except:
        #return ('We were not able to access Tribe at this moment')
        return []


def retrieve_public_versions(options={}):
    versions_url = 'http://' + TRIBE_URL + '/api/v1/version/?format=json&organism__slug=homo-sapiens'

    for opt_key,opt in options.iteritems():
        versions_url += '&'+opt_key+'='+opt

    try:
        tribe_connection = requests.get(versions_url)
        result = tribe_connection.json()
        versions = result['objects']
        return versions

    except:
        #return ('We were not able to access Tribe at this moment')
        return []

def retrieve_user_object(access_token):
    try:
        parameters = {'oauth_consumer_key': access_token}

        tribe_connection = requests.get('http://' + TRIBE_URL + '/api/v1/user', params = parameters)

        result = tribe_connection.json()
        user = result['objects']
        meta = result['meta']
        if (meta.has_key('oauth_token_expired')):
            return ('OAuth Token expired')
        else:
            return user
    except:
        #return ('We were not able to access Tribe at this moment')
        return []



def retrieve_user_genesets(access_token):

    try:
        parameters = {'oauth_consumer_key': access_token}

        user = retrieve_user_object(access_token)

        if (user == 'OAuth Token expired'):
            return ('OAuth Token expired')

        else:
            genesets_url = 'http://' + TRIBE_URL + '/api/v1/geneset/' + '?creator=' + str(user[0]['id'])
            tribe_connection = requests.get(genesets_url, params=parameters)
            result = tribe_connection.json()
            meta = result['meta']
            genesets = result['objects']
            return genesets

    except:
        #return ('We were not able to access Tribe at this moment')
        return []


def retrieve_user_versions(access_token, geneset):

    try:
        parameters = {'oauth_consumer_key': access_token}

        versions_url = 'http://' + TRIBE_URL + '/api/v1/version/?geneset__id=' + geneset + CROSSREF_DB
        tribe_connection = requests.get(versions_url, params=parameters)
        result = tribe_connection.json()
        meta = result['meta']
        versions = result['objects']
        return versions

    except:
        #return ('We were not able to access Tribe at this moment')
        return []

def retrieve_all_user_versions(access_token):

    try:
        parameters = {'oauth_consumer_key': access_token}

        versions_url = 'http://' + TRIBE_URL + '/api/v1/version/?' + CROSSREF_DB + '&show_tip=true'
        tribe_connection = requests.get(versions_url, params=parameters)
        result = tribe_connection.json()
        meta = result['meta']
        versions = result['objects']
        return versions

    except:
        #return ('We were not able to access Tribe at this moment')
        return []


#def return_gene_objects(gene_id_list):
#    gene_queryset = Gene.objects.filter(entrez__in=gene_id_list)
#    return gene_queryset


