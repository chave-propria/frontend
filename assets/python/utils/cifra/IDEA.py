from random import randint
from typing import Dict, List, Tuple

class IDEA:
    def __init__(self, rounds: int = 12) -> None:
        self.sub_blocks_keys = 13
        self.key_per_block = 6
        self.rounds = rounds


    def generate_key(self) -> Dict[int, List[int]]:
        chaves =  {
            sub: [randint(1, 65536) for _ in range(self.key_per_block)] 
            for sub in range(self.sub_blocks_keys)
        }

        return chaves


    def _key_math_operations(
        self,
        key: Dict[int, List[int]],
        info: List[int],
        vetor_inicial: List[int],
    ) -> Tuple[List[int], List[int]]:

        for _round in range(self.rounds):
            # Inicializa valores de p1 até p4
            p = [
                vetor * key[_round][index]
                for index, vetor in enumerate(vetor_inicial)
            ]

            p5, p6= p[0] ^ p[2], p[1] ^ p[3]

            p7 = p5 * key[_round][4]
            p8 = p6 + p7
            p9 = p8 * key[_round][5]
            p10 = p7 + p9

            if _round == 8:
                feedback = [
                    val ^ p9 if index in {0, 1} else val ^ p10
                    for index, val in enumerate(p)
                ]

        cif = [
            (vetor_inicial[index] * key[_round + 1][index]) ^ msg_value
            if index in {0, 3}
            else (vetor_inicial[index] + key[_round + 1][index]) ^ msg_value
            for index, msg_value in enumerate(info) 
        ]

        return (feedback, cif)


    def cifra(
        self,
        information: Dict[int, List[int]],
        key: Dict[int, List[int]],
    ) -> Dict[int, List[int]]:

        cif: Dict[int, List[int]] = {key: [] for key in information.keys()}
        feedback = [70 * sub_key for sub_key in key[0]]

        for block, sub_block in information.items():
            feedback, cifrado = self._key_math_operations(
                info=sub_block, vetor_inicial=feedback, key=key
            )
            cif[block].extend(cifrado)

        return cif
