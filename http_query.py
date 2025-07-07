import requests
from json import dumps, loads


URL = 'http://localhost:3080'


def serialize(request_body=None):
    """ The function returns a json objects """
    if request_body: return dumps(request_body)


def deserialize(content):
    """ The function returns a python objects """
    if content: return loads(content)


def post_method(api, headers, data=None):
    """ The function return -> Response """
    try:
        return requests.post(url=f'{URL}{api}', headers=headers, data=serialize(data))
    except Exception as e:
        return e


def delete_method(token, project_id):
    """ Deletes a previously created project """
    api = '/v3/projects/'
    headers = { 'accept':'*/*', 'Authorization':f'bearer {token}' }

    try:
        if requests.delete(url=f'{URL}{api}{project_id}', headers=headers).status_code == 204:
            return 'The project has been deleted successfully'
    except Exception as e:
        return e


def get_token():
    """
        The function gets a token for user authorization 
        re-challenge refreshes access token
    """
    authenticate = '/v3/access/users/authenticate'
    headers = { 'accept':'application/json', 'Content-Type':'application/json' }
    data = { 'username':'admin', 'password':'admin' }

    try:
        response = post_method(api=authenticate, headers=headers, data=data)
        if response.status_code == 200: return deserialize(response.content)['access_token']
    except Exception as e:
        return e


def create_project(token):
    """ The function creates a project """
    project = '/v3/projects/'
    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }
    data = { 'name':'Support IPv4' }

    try:
        response = post_method(api=project, headers=headers, data=data)
        if response.status_code == 201: return deserialize(response.content)['project_id']
    except Exception as e:
        return e


def statistic(token):
    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }
    return deserialize(requests.get(url=URL+'/v3/statistics', headers=headers).content)



"""def create_templates(token):
    api = '/v3/templates'
    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }

    clients = []
    for client in ('client1', 'client2'):
        data = { 'name':f'{client}', 'template_type':'vpcs' }
        response_body = ml.post_method(api=api, headers=headers, data=data).content
        clients.append(ml.deserialize(response_body))

    return clients
"""
