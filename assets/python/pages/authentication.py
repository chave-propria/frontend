from http import HTTPStatus
from json import loads

from js import console, document, fetch, URLSearchParams, window
from pyscript import when

from popup import pop_up


username = document.getElementById('username')
password = document.getElementById('password')
api_url = 'http://127.0.0.1:8000'  # TODO: Alterar para variável global

def error_login(text):
    error_msg = loads(text)
    pop_up.show_popup(message=error_msg["detail"])


def login_sucesso(text):
    window.location.href = '/html/contatos.html'


@when('submit', '#LoginForm')
def button(event):
    event.preventDefault()

    body = URLSearchParams.new(
        f'username={username.value}&password={password.value}'
    )

    def handle_response(response):
        if response.status != HTTPStatus.OK:
            response.text().then(error_login)
        else:
            response.text().then(login_sucesso)

    fetch(f'{api_url}/auth/token', body=body, method='POST', credentials='include').then(
        handle_response
    ).catch(lambda data: console.error(data))
