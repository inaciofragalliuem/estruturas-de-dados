from Estruturas.filaEstDin import FilaDinamica, TipoItem, deepcopy

class PilhaComFila():
    def __init__(self):
        self._fila1 = FilaDinamica()
        self._fila2 = FilaDinamica()
        self.item: TipoItem | None = None
        self._nItens = 0

    def cheia(self) -> bool:
        return False

    def vazia(self) -> bool:
        return self._fila1.vazia()

    def empilha(self, item: TipoItem) -> bool:
        self._fila1.enfileira(item)
        self._nItens += 1

        return True

    def desempilha(self) -> bool:
        if self.vazia():
            self.item = None
            return False

        for i in range(self._nItens - 1):
            self._fila1.desenfileira()
            self._fila2.enfileira(self._fila1.item)

        self._fila1.desenfileira()
        self.item = deepcopy(self._fila1.item)

        temp = self._fila1
        self._fila1 = self._fila2
        self._fila2 = temp

        self._nItens -= 1

        return True

    def topo(self) -> TipoItem:
        if self.vazia():
            return TipoItem()

        for i in range(self._nItens - 1):
            self._fila1.desenfileira()
            self._fila2.enfileira(self._fila1.item)

        self._fila1.desenfileira()
        item = deepcopy(self._fila1.item)
        self._fila2.enfileira(item)

        temp = self._fila1
        self._fila1 = self._fila2
        self._fila2 = temp

        return item

pf = PilhaComFila()

pf.empilha(TipoItem(20))
pf.empilha(TipoItem(40))

pf.desempilha()
print(pf.item)
print(pf.topo())