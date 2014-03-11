from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from tribe_client import utils
from .app_settings import TRIBE_ID, TRIBE_URL
import json


def connect_to_tribe(request):
    if 'tribe_token' not in request.session:
        return render(request, 'establish_connection.html', {'client_id': TRIBE_ID, 'tribe_url': TRIBE_URL})
    else:
        access_token = request.session['tribe_token']
        return display_genesets(request, access_token)

def logout_from_tribe(request):
    request.session.clear()
    return connect_to_tribe(request)

def access_genesets(request):
    access_code = request.GET.__getitem__('code')
    access_token = utils.get_access_token(access_code)
    request.session['tribe_token'] = access_token
    return display_genesets(request, access_token)

def display_genesets(request, access_token):
    is_token_valid = utils.retrieve_user_object(access_token)
    if (is_token_valid == 'OAuth Token expired'):
        request.session.clear()
        return connect_to_tribe(request)
    else:
        genesets = utils.retrieve_user_genesets(access_token)
        return render(request, 'display_genesets.html', {'genesets': genesets, 'access_token': access_token})

def display_versions(request, access_token, geneset):
    is_token_valid = utils.retrieve_user_object(access_token)

    if (is_token_valid == 'OAuth Token expired'):
        request.session.clear()
        return connect_to_tribe(request)
    else:
        versions = utils.retrieve_user_versions(access_token, geneset)
        for version in versions:
            version['gene_list'] = utils.return_gene_objects(version['genes'])
        return render(request, 'display_versions.html', {'versions': versions})

def return_access_token(request):
    data = {
        'access_token': request.session['tribe_token']
    }
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


