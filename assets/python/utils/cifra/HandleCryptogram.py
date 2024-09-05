from ast import literal_eval
from js import document, window
from typing import Any, Dict, List

from IDEA import IDEA


class HandleCryptogram:
    def __init__(self, ws) -> None:
        self.idea = IDEA()
        self.ws = ws
        self.ls = window.localStorage


    def __common_crypt(
        self,
        jump: int,
        cryptogram: Dict[int, List[int]],
        temp_key: Dict[int, List[int]],
    ) -> Dict[str, Any]:
        """
        Realiza o processo de cifração

        Se o processo for executado um número par de vezes, com a mesma chave, é obtido o texto plano

        Arguments:
            jump (int): O estágio de envio da mensagem
            cryptogram (Dict[int, List[int]]): O criptograma que será utilizado
            temp_key (Dict[int, List[int]]): A chave que será utilizada na cifração
 
        Returns:
            Dict[str, Any]: Um dicionário com o criptograma ou a mensagem decifrada
        """
        crypt = self.idea.cifra(information=cryptogram, key=temp_key)
        resend = {'jump': (jump + 1), 'cif': crypt}

        return resend


    def encryption(
        self, jump: int, cryptogram: Dict[int, List[int]]
    ) -> None:
        temp_key = self.idea.generate_key()
        self.ls.setItem("temp_key", temp_key)

        resend = self.__common_crypt(
            jump=jump, cryptogram=cryptogram, temp_key=temp_key
        )

        self.ws.send(resend)


    def decryption(
        self, jump: int, cryptogram: Dict[int, List[int]]
    ) -> None:
        temp_key = literal_eval(self.ls.getItem("temp_key"))

        resend  = self.__common_crypt(
            jump=jump, cryptogram=cryptogram, temp_key=temp_key
        )

        self.ws.send(resend)

    
    def display_msg(
        self, jump: int, cryptogram: Dict[int, List[int]]
    ) -> None:
        temp_key = literal_eval(self.ls.getItem("temp_key"))

        msg = self.__common_crypt(
            jump=jump, cryptogram=cryptogram, temp_key=temp_key
        )

        msg_to_display = [
            bytes.fromhex(hex(msg)[2:]).decode()
            for msg_block in msg['cif'].values() for msg in msg_block
        ]

        messages = document.getElementById('chat-messages')

        message = document.createElement('p')
        message.innerText = ''.join(msg_to_display)
        messages.append(message)
