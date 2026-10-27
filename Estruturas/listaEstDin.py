from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

_TERRA = -1

LISTA_VAZIA = 1
LISTA_CHEIA = 2
ITEM_EXISTENTE = 3
ITEM_INEXISTENTE = 4

@dataclass
class TipoItem:
    nome: str | None = None
    cpf: str | None = None
    idade: int | None = None

@dataclass
class TipoNoEst:
    item: TipoItem | None = None
    _prox: int | None = None
    

class ListaEstaticaEncadeada():
    def __init__(self, maxTam):
        self._maxTam = maxTam
        self._lista = [ TipoNoEst() for i in range(self._maxTam) ]
        self._inicio = _TERRA
        self._livres = 0
        self._nItens = 0
        self._opSt = LISTA_VAZIA
        for pos in range(self._maxTam - 1):
            self._lista[pos]._prox = pos + 1
        self._lista[self._maxTam - 1]._prox = _TERRA
        self.item: TipoItem | None = None

    def cheia(self) -> bool:
        return self._nItens == self._maxTam

    def vazia(self) -> bool:
        return self._nItens == 0

    def opStatus(self) -> int:
        return self._opSt

    def totalItens(self) -> int:
        return self._nItens

    def _buscaItem(self, nome: str) -> int:
        if self.vazia():
            self._opSt = ITEM_INEXISTENTE
            return _TERRA

        posAnt = _TERRA
        atual = self._inicio
        achou = False
        fimCurso = False

        while not achou and not fimCurso:
            achou = nome <= self._lista[atual].item.nome

            if not achou:
                posAnt = atual
                atual = self._lista[atual]._prox
                fimCurso = atual == _TERRA

        if not achou or nome < self._lista[atual].item.nome:
            self._opSt = ITEM_INEXISTENTE
        else:
            self._opSt = ITEM_EXISTENTE

        return posAnt

    def inserir(self, item: TipoItem) -> bool:
        if self.cheia():
            self._opSt = LISTA_CHEIA
            return False

        posAnt = self._buscaItem(item.nome)

        if self._opSt == ITEM_EXISTENTE:
            return False

        posLivre = self._livres
        self._livres = self._lista[self._livres]._prox
        self._lista[posLivre].item = deepcopy(item)

        if posAnt == _TERRA:
            self._lista[posLivre]._prox = self._inicio
            self._inicio = posLivre
        else:
            self._lista[posLivre]._prox = self._lista[posAnt]._prox
            self._lista[posAnt]._prox = posLivre

        self._nItens += 1

        return True

    def remover(self, nome: str) -> bool:
        posAnt = self._buscaItem(nome)

        if self._opSt == ITEM_INEXISTENTE:
            self.item = None
            return False

        if posAnt == _TERRA:
            aux = self._inicio
            self._inicio = self._lista[aux]._prox
        else:
            aux = self._lista[posAnt]._prox
            self._lista[posAnt]._prox = self._lista[aux]._prox

        self.item = deepcopy(self._lista[aux].item)
        self._lista[aux]._prox = self._livres
        self._livres = aux
        self._nItens -= 1

        return True

    def mostrar(self) -> None:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            return

        pos = self._inicio
        while pos != _TERRA:
            print(pos,":")
            print("Nome:",self._lista[pos].item.nome)
            print("CPF:",self._lista[pos].item.cpf)
            print("Idade:",self._lista[pos].item.idade)
            pos = self._lista[pos]._prox

    def consultar(self, nome: str) -> bool:
        posAnt = self._buscaItem(nome)

        if self._opSt == ITEM_INEXISTENTE:
            self.item = None
            return False

        if posAnt == _TERRA:
            self.item = deepcopy(self._lista[self._inicio].item)
        else:
            self.item = deepcopy(self._lista[self._lista[posAnt]._prox].item)

        return True

    def atualizar(self, item: TipoItem) -> int:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            return self._opSt

        posAnt = self._buscaItem(item.nome)

        if self._opSt == ITEM_INEXISTENTE:
            return self._opSt

        if posAnt == _TERRA:
            self._lista[self._inicio].item.cpf = item.cpf
            self._lista[self._inicio].item.idade = item.idade
        else:
            self._lista[self._lista[posAnt]._prox].item.cpf = item.cpf
            self._lista[self._lista[posAnt]._prox].item.idade = item.idade

        return ITEM_EXISTENTE

    def reiniciar(self) -> None:
        self._inicio = _TERRA
        self._livres = 0
        self._nItens = 0
        self._opSt = LISTA_VAZIA
        for pos in range(self._maxTam - 1):
            self._lista[pos]._prox = pos + 1
        self._lista[self._maxTam - 1]._prox = _TERRA
        self.item: TipoItem | None = None

    def reordenaCpf(self) -> None:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            return

        for i in range(self._nItens - 1):
            posAnt = _TERRA
            atual = self._inicio

            while self._lista[atual]._prox != _TERRA:
                seguinte = self._lista[atual]._prox

                if self._lista[atual].item.cpf > self._lista[seguinte].item.cpf:
                    print("Trocando de lugar")
                    self._lista[atual]._prox = self._lista[seguinte]._prox
                    self._lista[seguinte]._prox = atual

                    if posAnt == _TERRA:
                        self._inicio = seguinte
                    else:
                        self._lista[posAnt]._prox = seguinte

                    posAnt = seguinte

                else:
                    posAnt = atual
                    atual = seguinte

LISTA_VAZIA = 1
LISTA_CHEIA = 2
ITEM_EXISTENTE = 3
ITEM_INEXISTENTE = 4

@dataclass
class TipoNoDin:
    item: TipoItem | None = None
    _prox: TipoNoDin | None = None
    _ant: TipoNoDin | None = None

class ListaDinamicaBi():
    def __init__(self):
        self._nItens = 0
        self._inicio: TipoNoDin | None = None
        self._opSt = LISTA_VAZIA
        self.item: TipoItem | None = None

    def vazia(self) -> bool:
        return self._inicio == None

    def cheia(self) -> bool:
        return False

    def opStatus(self) -> int:
        return self._opSt

    def totalItens(self) -> int:
        return self._nItens

    def _buscaItem(self, nome: str) -> TipoNoDin:
        if self.vazia():
            self._opSt = ITEM_INEXISTENTE
            return None

        posAnt: TipoNoDin | None = None
        atual = self._inicio
        achou = False
        fimCurso = False

        while not achou and not fimCurso:
            achou = nome <= atual.item.nome

            if not achou:
                posAnt = atual
                atual = atual._prox
                fimCurso = atual == None

        if not achou or nome < atual.item.nome:
            self._opSt = ITEM_INEXISTENTE
        else:
            self._opSt = ITEM_EXISTENTE

        return posAnt

    def insere(self, item: TipoItem) -> bool:
        if self.cheia():
            self._opSt = LISTA_CHEIA
            return False

        posAnt: TipoNoDin = self._buscaItem(item.nome)

        if self._opSt == ITEM_EXISTENTE:
            return False

        posLivre: TipoNoDin = TipoNoDin()
        posLivre.item = deepcopy(item)

        if posAnt == None:
            posLivre._prox = self._inicio
            posLivre._ant = None

            if not self.vazia():
                self._inicio._ant = posLivre
            
            self._inicio = posLivre
        elif posAnt._prox == None:
            posLivre._prox = None
            posLivre._ant = posAnt
            posAnt._prox = posLivre
        else:
            posLivre._prox = posAnt._prox
            posLivre._ant = posAnt
            posAnt._prox._ant = posLivre
            posAnt._prox = posLivre

        self._nItens += 1

        return True

    def remove(self, nome: str) -> bool:
        posAnt = self._buscaItem(nome)

        if self._opSt == ITEM_INEXISTENTE:
            self.item = None
            return False

        if posAnt == None:
            aux = self._inicio
            self._inicio = aux._prox
            if aux._prox != None:
                self._inicio._ant = None

        elif posAnt._prox._prox == None:
            aux = posAnt._prox
            posAnt._prox = None
        else:
            aux = posAnt._prox
            posAnt._prox = aux._prox
            posAnt._prox._ant = posAnt

        aux._prox = None
        aux._ant = None
        self.item = deepcopy(aux.item)

        self._nItens -= 1

        return True

    def mostrar(self) -> None:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            return

        pos = self._inicio
        while pos != None:
            print(pos + ":")
            print(f"Anterior: {pos._ant} - Próximo: {pos._prox}")
            print("Nome:",self._lista[pos].item.nome)
            print("CPF:",self._lista[pos].item.cpf)
            print("Idade:",self._lista[pos].item.idade)
            pos = self._lista[pos]._prox

    def reordenaCpf(self) -> None:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            return

        for i in range(self._nItens - 1):
            posAnt: TipoNoDin | None = None
            atual = self._inicio

            while atual._prox != None:
                seguinte = atual._prox

                if atual.item.cpf > seguinte.item.cpf:
                    atual._prox = seguinte._prox

                    if atual._prox != None:
                        atual._prox._ant = atual
                        
                    seguinte._ant = atual._ant
                    atual._ant = seguinte
                    seguinte._prox = atual

                    if posAnt == None:
                        self._inicio = seguinte
                    else:
                        posAnt._prox = seguinte

                    posAnt = seguinte

                else:
                    posAnt = atual
                    atual = seguinte