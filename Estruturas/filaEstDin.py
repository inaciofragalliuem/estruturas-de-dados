from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

_TERRA: int = -1

@dataclass
class TipoItem():
    valor: int | float | str | None = None

class FilaEstatica():
    def __init__(self, tamMax: int):
        self._tamMax = tamMax
        self._fila = [ TipoItem() for _ in range(tamMax) ]
        self._inicio = 0
        self._fim = _TERRA
        self._nItens = 0
        self.item = TipoItem()

    def vazia(self) -> bool:
        return self._fim == _TERRA

    def cheia(self) -> bool:
        return self._fim == self._tamMax - 1

    def enfileira(self, item: TipoItem) -> bool:
        if self.cheia():
            return False

        self._fim = (self._fim + 1) % self._tamMax
        self._fila[self._fim] = deepcopy(item)
        self._nItens += 1

        return True

    def desenfileira(self) -> bool:
        if self.vazia():
            self.item = TipoItem()
            return False

        self.item = self._fila[self._inicio]
        self._inicio = (self._inicio + 1) % self._tamMax
        self._nItens -= 1

        return True

    def primeiroItem(self) -> TipoItem:
        if self.vazia():
            self.item = TipoItem()
            return self.item

        return self._fila[self._inicio]

    def mostra(self) -> None:
        if self.vazia():
            print("A fila está vazia!")
            return

        print("Situação da Fila:")

        aux = self._fim
        qtd = self._nItens

        while qtd > 0:
            print(self._fila[aux].valor, ", ", end="")
            aux = (aux + 1) % self._tamMax
            qtd -= 1

    def esvazia(self) -> None:
        self._inicio = 0
        self._fim = _TERRA
        self._nItens = 0
        self.item = TipoItem()

@dataclass
class TipoNo:
    item: TipoItem | None = None
    _prox: TipoNo | None = None

class FilaDinamica():
    def __init__(self):
        self.item: TipoItem | None = None
        self._primeiro: TipoNo | None = None
        self._ultimo: TipoNo | None = None
        self._nItens = 0

    def vazia(self) -> bool:
        return self._primeiro == None

    def cheia(self) -> bool:
        return False

    def enfileira(self, item: TipoItem) -> bool:
        novoNo: TipoNo = TipoNo()
        novoNo.item = deepcopy(item)

        if self.vazia():
            self._primeiro = novoNo
        else:
            self._ultimo._prox = novoNo

        self._ultimo = novoNo
        self._nItens += 1

        return True

    def desenfileira(self) -> bool:
        if self.vazia():
            self.item = TipoItem()
            return False

        self.item = deepcopy(self._primeiro.item)
        self._primeiro = self._primeiro._prox
        self._nItens -= 1

        if self._primeiro == None:
            self._ultimo = None

        return True

    def primeiroItem(self) -> TipoItem:
        if self.vazia():
            self.item = TipoItem()
            return self.item

        return deepcopy(self._primeiro.item)

    def mostra(self) -> None:
        if self.vazia():
            print("A fila está vazia!")
            return

        print("Situação da fila:")

        pos = self._primeiro
        while pos != None:
            print(pos.item.valor, end="")

            pos = pos._prox

            if pos != None:
                print(", ", end="")

        print()

    def esvazia(self) -> None:
        self._primeiro = None
        self._ultimo = None
        self._nItens = 0
        self.item = None


fila = FilaDinamica()

fila.enfileira(TipoItem(20))
fila.enfileira(TipoItem(40))

fila.desenfileira()
print("Primeiro:", fila.item)

fila.desenfileira()
print("Segundo:", fila.item)