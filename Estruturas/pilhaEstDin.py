from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

_TERRA = -1

@dataclass
class TipoItem:
    valor: int | float | str | None = None

class PilhaEstatica():
    def __init__(self, tamMax):
        self._tamMax = tamMax
        self._pilha: list[TipoItem] = [ TipoItem() for _ in range(tamMax) ]
        self._topo = _TERRA
        self.item = TipoItem()

    def cheia(self) -> bool:
        return self._topo == self._tamMax - 1

    def vazia(self) -> bool:
        return self._topo == _TERRA

    def empilha(self, item: TipoItem) -> bool:
        if self.cheia():
            return False

        self._topo += 1
        self._pilha[self._topo] = item

        return True

    def desempilha(self) -> bool:
        if self.vazia():
            self.item = TipoItem()
            return False

        self.item = deepcopy(self._pilha[self._topo])
        self._topo -= 1

        return True

    def topo(self) -> TipoItem:
        if self.vazia():
            return TipoItem()

        return deepcopy(self._pilha[self._topo])

    def mostra(self) -> None:
        print("A pilha está vazia!") if self.vazia() else print("Situação da pilha:")

        for i in range(self._topo + 1):
            print(self._pilha[i].valor, end="")

    def esvazia(self) -> None:
        self._topo = _TERRA
        self.item = TipoItem()


@dataclass
class _TipoNo:
    item: TipoItem | None = None
    _prox: _TipoNo | None = None

class PilhaDinamica():
    def __init__(self):
        self.item: TipoItem | None = None
        self._topo: _TipoNo | None = None

    def cheia(self) -> bool:
        return False

    def vazia(self) -> bool:
        return self._topo == None

    def empilha(self, item: TipoItem) -> bool:
        if self.cheia():
            return False

        novoNo: _TipoNo = _TipoNo()
        novoNo.item = deepcopy(item)
        novoNo._prox = self._topo
        self._topo = novoNo

        return True

    def desempilha(self) -> bool:
        if self.vazia():
            self.item = None
            return False

        self.item = deepcopy(self._topo.item)
        aux = self._topo
        self._topo = self._topo._prox
        aux._prox = None

        return True

    def topo(self) -> TipoItem:
        if self.vazia():
            return TipoItem

        return deepcopy(self._topo.item)

    def mostra(self) -> None:
        print("A pilha está vazia!") if self.vazia() else print("Situação da pilha:")

        pos = self._topo
        while pos != None:
            print(pos.item.valor, " ")
            pos = pos._prox

    def esvazia(self) -> None:
        self._topo = None
        self.item = None