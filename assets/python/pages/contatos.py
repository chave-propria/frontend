from http import HTTPStatus
from json import loads

from js import console, document, fetch

contatos_list = document.getElementById('listaContatos')

api_url = 'http://127.0.0.1:8000' # TODO: Alterar para variável global


def error(response):
    console.error(response)

def get_info(response):
    contatos = loads(response)

    for contato in contatos:
        li = document.createElement('li')

        a = document.createElement('a')
        a.href = f'/html/webchat.html?email={contato['email']}'
        a.textContent = contato['email']

        li.appendChild(a)
        contatos_list.append(li)


def handle_response(response):
    if response.status != HTTPStatus.OK:
        response.text().then(error)
    else:
        response.text().then(get_info)

fetch(
    f'{api_url}/contatos/convites?status=accepted&limite=10',
    method='GET',
    credentials='include',
).then( handle_response ).catch(lambda data: console.error(data))
