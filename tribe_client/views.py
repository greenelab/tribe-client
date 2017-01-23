import os
import itertools
import json
import logging
import pickle

from collections import defaultdict

from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.utils import html

from tribe_client import utils

from app_settings import (
    TRIBE_URL, TRIBE_ID, TRIBE_SCOPE, ACCESS_CODE_URL,
    BASE_TEMPLATE, TRIBE_LOGIN_REDIRECT, TRIBE_LOGOUT_REDIRECT,
    CROSSREF, PUBLIC_GENESET_FOLDER
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def connect_to_tribe(request):
    if 'tribe_token' not in request.session:
        return render(request, 'establish_connection.html',
                      {'tribe_url': TRIBE_URL,
                       'access_code_url': ACCESS_CODE_URL,
                       'client_id': TRIBE_ID,
                       'scope': TRIBE_SCOPE,
                       'base_template': BASE_TEMPLATE})
    else:
        return display_genesets(request)


def get_settings(request):
    tribe_settings = {'tribe_url': TRIBE_URL,
                      'access_code_url': ACCESS_CODE_URL,
                      'client_id': TRIBE_ID,
                      'scope': TRIBE_SCOPE}

    json_response = json.dumps(tribe_settings)
    return HttpResponse(json_response, content_type='application/json')


def logout_from_tribe(request):
    request.session.clear()

    if TRIBE_LOGOUT_REDIRECT:
        return HttpResponseRedirect(TRIBE_LOGOUT_REDIRECT)
    else:
        return connect_to_tribe(request)


def get_token(request):
    access_code = request.GET.__getitem__('code')
    access_token = utils.get_access_token(access_code)
    request.session['tribe_token'] = access_token
    request.session['tribe_user'] = utils.retrieve_user_object(access_token)

    if TRIBE_LOGIN_REDIRECT:
        return HttpResponseRedirect(TRIBE_LOGIN_REDIRECT)
    else:
        return redirect('display_genesets')


def display_genesets(request):
    if 'tribe_token' in request.session:
        access_token = request.session['tribe_token']
        get_user = utils.retrieve_user_object(access_token)

        if (get_user == 'OAuth Token expired' or get_user == []):
            request.session.clear()
            return connect_to_tribe(request)

        else:  # The user must be logged in and has access to her/himself
            genesets = utils.retrieve_user_genesets(
                access_token, {'full_genes': 'true', 'limit': 100})
            tribe_user = get_user
            return render(request, 'display_genesets.html',
                          {'tribe_url': TRIBE_URL,
                           'genesets': genesets,
                           'tribe_user': tribe_user,
                           'base_template': BASE_TEMPLATE})

    else:
        return connect_to_tribe(request)


def display_versions(request, geneset):
    if 'tribe_token' in request.session:
        access_token = request.session['tribe_token']
        get_user = utils.retrieve_user_object(access_token)

        if (get_user == 'OAuth Token expired' or get_user == []):
            request.session.clear()
            return connect_to_tribe(request)

        else:
            versions = utils.retrieve_user_versions(access_token, geneset)
            for version in versions:
                version['gene_list'] = []
                for annotation in version['annotations']:
                    version['gene_list'].append(
                            annotation['gene']['standard_name'])
            return render(request, 'display_versions.html',
                          {'versions': versions,
                           'base_template': BASE_TEMPLATE})


def return_access_token(request):
    if 'tribe_token' in request.session:
        data = {'access_token': request.session['tribe_token']}
    else:
        data = {'access_token': 'No access token'}
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def create_geneset(request):
    """
    View to handle the creation of genesets on Tribe when users make
    POST request to the '/tribe_client/create_geneset' URL.

    Arguments:
    request -- Request object, which contains a dictionary-like object
    of POST data, among other things.

    * In the POST data, there should be a 'geneset' object that contains
    the information for the geneset being created. This 'geneset' is
    passed in the POST data as a string, which we load as json to get a
    dictionary. The general format for the data in this geneset object is:

    geneset = {
        organism: 'Mus musculus',  # Required
        title: 'Sample title',  # Required

        abstract: 'Sample abstract',  # Optional

        # Genes to be included in the geneset are sent in the 'annotations'
        # dictionary, and this whole dictionary is optional. The geneset
        # can have as many or as few annotations as desired. The format for
        # the annotations dictionary is:
        # {gene_id1: [<list of pubmed ids associated with that gene>],
        #  gene_id2: [<list of pubmed ids associated with that gene>]...}
        # The type of identifier for the gene_ids is whatever is set
        # in the CROSSREF setting.
        annotations: {55982: [20671152, 19583951],
                      18091: [8887666], 67087: [],
                      22410:[]}
    }

    Returns:
    Either -

    a) The Tribe URL of the geneset that has just been created, or
    b) A 401 Unauthorized response if the user is not signed in

    N.B. To gracefully save to Tribe, your interface should handle the
    case when a 400 and 401 responses are returned. One way to do this
    for the 401 Unauthorized response, for example, is to catch the error
    and send the user to the Tribe-login page ('/tribe_client' url, which
    is named 'connect_to_tribe' in urls.py). Another way to handle this
    response is to only allow the users to make a request
    to this view (via a button, etc.) when they are already signed in.

    """
    if not ('tribe_token' in request.session):
        return HttpResponse('Unauthorized', status=401)

    tribe_token = request.session['tribe_token']
    is_token_valid = utils.retrieve_user_object(tribe_token)

    if (is_token_valid == 'OAuth Token expired'):
        request.session.clear()
        return HttpResponse('Unauthorized', status=401)

    geneset_info = request.POST.get('geneset')
    geneset_info = json.loads(geneset_info)
    geneset_info['xrdb'] = CROSSREF

    tribe_response = utils.create_remote_geneset(tribe_token, geneset_info,
                                                 TRIBE_URL)
    try:
        slug = tribe_response['slug']
        creator = tribe_response['creator']['username']
        geneset_url = TRIBE_URL + "/#/use/detail/" + creator + "/" + slug
        html_safe_content = html.escape(geneset_url)
        response = {'geneset_url': html_safe_content}

    # If there is an error and a json object could not be loaded from the
    # response, the create_remote_geneset() util function will return a
    # raw response from Tribe, which will trigger a TypeError when trying
    # to access a key from it like a dictionary.
    except TypeError:
        html_safe_content = html.escape(tribe_response.content)
        return HttpResponseBadRequest('The following error has been returned'
                                      ' by Tribe while attempting to create '
                                      'a geneset: "' + html_safe_content +
                                      '"')

    json_response = json.dumps(response)
    return HttpResponse(json_response, content_type='application/json')


def return_user_obj(request):

    if 'tribe_token' in request.session:
        tribe_token = request.session['tribe_token']

    else:
        tribe_token = None

    tribe_response = utils.return_user_object(tribe_token)

    json_response = json.dumps(tribe_response)
    return HttpResponse(json_response, content_type='application/json')


def return_unpickled_genesets(request):
    organism = request.GET.get('organism')

    if not organism:
        logger.error(
            'No organism was sent in request made to '
            'return_unpickled_genesets() function.')
        return HttpResponseBadRequest(
            "No organism scientific name was sent in the request. Please "
            "specify an organism's scientific name (e.g. 'Pseudomonas "
            "aeruginosa' or 'Homo sapiens') using the 'organism' parameter.")

    pickled_filename = organism.replace(' ', '_') + '_pickled_genesets'

    public_genesets = {}
    if PUBLIC_GENESET_FOLDER:
        pickled_filename_path = os.path.join(
            PUBLIC_GENESET_FOLDER, pickled_filename)

        if os.path.exists(pickled_filename_path):
            unpickled_contents = pickle.load(open(pickled_filename_path))
            public_genesets = unpickled_contents[0]
        else:
            logger.error(
                ('No pickled genesets file was found for organism with '
                 'scientific name {0} in return_unpickled_genesets() '
                 'function').format(organism))

    else:
        logger.error(
            'return_unpickled_genesets function was called, but '
            'PUBLIC_GENESET_FOLDER setting has not been defined.')

    usergenesets = {}
    if 'tribe_genesets' in request.session:
        usergenesets['My Gene Sets'] = request.session['tribe_genesets']
    elif 'tribe_token' in request.session:
        tribe_token = request.session['tribe_token']
        usergenesets['My Gene Sets'] = utils.retrieve_user_genesets(tribe_token)

    all_genes = set()

    geneset_dict, gene_dict = defaultdict(dict), defaultdict(set)

    for database, genesets in itertools.chain(public_genesets.iteritems(),
                                              usergenesets.iteritems()):
        for geneset in genesets:

            if 'tip' not in geneset or geneset['tip'] is None:
                continue

            geneset_id = str(geneset['id'])
            title = geneset['title']
            url = geneset['url'] if 'url' in geneset else ''

            if 'genes' in geneset['tip']:
                genes = set(geneset['tip']['genes'])
            else:
                genes = set()

            all_genes |= genes

            geneset_dict[geneset_id] = {'name': title, 'dbase': database,
                                        'url': url, 'size': len(genes)}
            for g in genes:
                gene_dict[str(g)].add(geneset_id)

    gene_dict = {
        gene: list(gs_set) for (gene, gs_set) in gene_dict.iteritems()
    }

    response_dict = {'procs': geneset_dict, 'genes': gene_dict,
                     'bgtotal': len(all_genes)}
    json_response = json.dumps(response_dict)

    return HttpResponse(json_response, content_type='application/json')
