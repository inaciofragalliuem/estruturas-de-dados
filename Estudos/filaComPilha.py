from pilhaEstDin import PilhaDinamica, TipoItem, deepcopy

class FilaComPilha:
    def __init__(self):
        self._entrada = PilhaDinamica()
        self._saida = PilhaDinamica()
        self._nItens = 0
        self.item: TipoItem | None = None

    def vazia(self) -> bool:
        return self._entrada.vazia() and self._saida.vazia()

    def cheia(self) -> bool:
        return False

    def enfileira(self, item: TipoItem) -> bool:
        self._entrada.empilha(item)
        self._nItens += 1
        return True

    def desenfileira(self) -> bool:
        if self._entrada.vazia() and self._saida.vazia():
            self.item = TipoItem()
            return False

        if self._saida.vazia():
            while not self._entrada.vazia():
                self._entrada.desempilha()
                self._saida.empilha(self._entrada.item)

        self._saida.desempilha()
        self.item = deepcopy(self._saida.item)
        self._nItens -= 1

        return True

    def primeiroItem(self) -> TipoItem:
        if self.vazia():
            return None

        if self._saida.vazia():
            self._entrada.desempilha()
            self._saida.empilha(self._entrada.item)

            return deepcopy(self._saida.topo())

        return deepcopy(self._saida.topo())