from ast import literal_eval

from js import console, document, WebSocket, URLSearchParams, window
from pyscript import when
from pyodide.ffi.wrappers import add_event_listener


from HandleCryptogram import HandleCryptogram
from InfoBlocks import InfoBlocks
from popup import pop_up

msg_document = document.getElementById('message-input')

query_string = window.location.search

# Converte a query string em um objeto URLSearchParams
params = URLSearchParams.new(query_string)

# Exemplo de obtenção de um parâmetro específico
user_email = params.get("email")

ws = WebSocket.new(f'ws://127.0.0.1:8000/ws/communicate/?user_email={user_email}')  # TODO: Alterar para variável global

ls = window.localStorage


# Quando receber uma mensagem
def ws_msg(event) -> None:
    """
    Função utilizada quando ocorrer algum evento de envio de mensagem via WebSocket
    A mensagem enviada, via WebSocket, sensibiliza está ação.
    """
    msg_json = literal_eval(event.data)
    jumps, msg = msg_json['jump'], msg_json['cif']

    handle_cryptogram = HandleCryptogram(ws=ws)
 
    ACTIONS_MAP = {
        2: handle_cryptogram.encryption,
        3: handle_cryptogram.decryption,
        4: handle_cryptogram.display_msg,
    }

    action = ACTIONS_MAP.get(jumps + 1)

    if action:
        action(jump=jumps, cryptogram=msg)


# Registra os eventos para `onOpen` e `onMessage` e `onClose`
add_event_listener(ws, 'open', lambda event: console.log('WebSocket conectado'))
add_event_listener(ws, 'close', lambda event: pop_up.show_popup(message=event.reason))
add_event_listener(ws, 'message', ws_msg)


# Quando houver um evento de `click` no objeto `send-button`
@when('click', '#send-button')
def message(event) -> None:

    # Criar chave e cifrar informação
    message: str = msg_document.value
    message_hex = [item.encode().hex() for item in message]

    handle_cryptogram = HandleCryptogram(ws=ws)
    handle_blocks = InfoBlocks()

    blocos = handle_blocks.info_blocks(msg=message_hex)

    handle_cryptogram.encryption(jump=0, cryptogram=blocos)
