from typing import Dict, List

class InfoBlocks:
    def __init__(self) -> None:
        self.qnt_bytes_bloco = 8


    def _bytes_faltantes(self, tam_msg: int) -> int:
        """
        Função privada utilizada para calcular os bytes faltantes para completar blocos

        Arguments:
            tam_msg (int): O tamanho do arquivo em bytes

        Returns:
            A quantidade de bytes faltantes
        """
        if tam_msg % self.qnt_bytes_bloco == 0:
            return 0

        if tam_msg <= self.qnt_bytes_bloco:
            return self.qnt_bytes_bloco - tam_msg

        return self.qnt_bytes_bloco - (tam_msg % self.qnt_bytes_bloco)


    def _sub_blocks_info(
        self,
        msg_blocks: List[List[str]]
    ) -> Dict[int, List[int]]:

        sub_blocks = {
            block: [
                int(''.join(sub_block[index : index + 2]), 16)
                for index in range(0, len(sub_block), 2)
            ] for block, sub_block in enumerate(msg_blocks)
        }

        return sub_blocks


    def _completa_bloco(
        self, bytes_faltantes: int, info: List[int]
    ) -> List[List[int]]:
        """
        Função privada utilizada para completar o bloco

        Arguments:
            bytes_faltantes (int): A quantidade de bytes faltantes
            info (List[int]): Os bytes de informação que serão utilizados no bloco

        Returns:
            O bloco de informação completo
        """
        completar_bloco = [
            chr(88).encode().hex() for _ in range(bytes_faltantes)
        ]

        completar_bloco.extend(info)

        return [
            completar_bloco[i: i + 8]
            for i in range(0, len(completar_bloco), 8)
        ]


    def info_blocks(self, msg: List[str]) -> Dict[int, List[int]]:
        bytes_faltantes = self._bytes_faltantes(tam_msg=len(msg))
        bloco_completo = list()

        if bytes_faltantes:
            read_bytes = (self.qnt_bytes_bloco - bytes_faltantes)
            info = msg[:read_bytes]

            del msg[:read_bytes]

            bloco_completo = self._completa_bloco(
                bytes_faltantes=bytes_faltantes, info=info
            )

        msg_block = [
            msg[i: i + self.qnt_bytes_bloco]
            for i in range(0, len(msg), self.qnt_bytes_bloco)
        ]

        bloco_completo.extend(msg_block)

        blocos = self._sub_blocks_info(msg_blocks=bloco_completo)

        return blocos
