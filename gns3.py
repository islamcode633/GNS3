import http_query as HTTP_query
import requests
from time import sleep


def getinfo_aboute_templates(token):
    api = f'/v3/templates/'
    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }
    response = requests.get(url=f'{HTTP_query.URL}{api}', headers=headers).content
    return HTTP_query.deserialize(response)


def get_template(data):
    for i in range(len(data)):
        if data[i]['template_type'] == 'vpcs':
            vpcs_template_id = data[i]['template_id']

        if data[i]['template_type'] == 'cloud':
            cloud_template_id = data[i]['template_id']

    return vpcs_template_id, cloud_template_id


def create_node(project_id, token, vpcs_template_id=None, cloud_template_id=None):
    if vpcs_template_id:
        api = f'/v3/projects/{project_id}/templates/{vpcs_template_id}'
    if cloud_template_id:
        api = f'/v3/projects/{project_id}/templates/{cloud_template_id}'

    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }
    data = { 'x':300, 'y':300 }

    response = HTTP_query.post_method(api=api, headers=headers, data=data)
    if response.status_code == 201:
        return HTTP_query.deserialize(response.content)


def parser_pc(personal_comp):
    node_id = personal_comp['node_id'] if personal_comp['node_id'] else False
    # value 0
    adapter_number = personal_comp['ports'][0]['adapter_number'] if not personal_comp['ports'][0]['adapter_number'] else False
    port_number = personal_comp['ports'][0]['port_number'] if not personal_comp['ports'][0]['port_number'] else False
    #
    if node_id and not adapter_number and not port_number:
        return [node_id, adapter_number, port_number]


def parser_cloud(cloud):
    node_id = cloud['node_id'] if cloud['node_id'] else False
    adapter_number = cloud['ports'][0]['adapter_number'] if not cloud['ports'][0]['adapter_number'] else False
    port_number = cloud['ports'][0]['port_number'] if not cloud['ports'][0]['port_number'] else False

    if node_id and not adapter_number and not port_number:
        return [node_id, adapter_number, port_number]


def creating_nodes(project_id, token):
    vpcs_template_id, cloud_template_id = get_template(getinfo_aboute_templates(token))
    vpcs = parser_pc(create_node(project_id=project_id, token=token, vpcs_template_id=vpcs_template_id))
    cloud = parser_cloud(create_node(project_id=project_id, token=token, cloud_template_id=cloud_template_id))

    return vpcs, cloud


def linking(project_id, token, node1, node2):
    api = f'/v3/projects/{project_id}/links'
    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }
    data = { 'nodes': [
            {   
                'node_id':f'{node1[0]}',
                'adapter_number': f'{node1[1]}',
                'port_number': f'{node1[2]}',
                "label": { "text": "eth0" }
            },
            {
                'node_id':f'{node2[0]}',
                'adapter_number': f'{node2[1]}',
                'port_number': f'{node2[2]}',
                "label": { "text": "br0" }
            }
        ]
    }

    response = HTTP_query.post_method(api=api, headers=headers, data=data)
    return HTTP_query.deserialize(response.content)


def start_node(project_id, node_id, token):
    api = f'/v3/projects/{project_id}/nodes/{node_id}/start'
    headers = { 'accept':'application/json', 'Authorization':f'bearer {token}', 'Content-Type':'application/json' }

    HTTP_query.deserialize(requests.post(url=f'{HTTP_query.URL}{api}', headers=headers, data='{}').content)


token = HTTP_query.get_token()
project_id = HTTP_query.create_project(token)
vpcs, cloud = creating_nodes(project_id=project_id, token=token)
linking(project_id=project_id, token=token, node1=vpcs, node2=cloud)
start_node(project_id=project_id, node_id=vpcs[0], token=token)


#sleep(20)
#print(ml.delete_method(token=token, project_id=project_id))
