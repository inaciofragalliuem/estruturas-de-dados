from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass

ACOUGUE = 1
PADARIA = 2
FRIOS_LATICINIOS = 3
HIGIENE_CORPORAL = 4
LIMPEZA_CASA = 5
HORTIFRUTI = 6
GRAOS_FARINACEOS_CAFE = 7
BEBIDAS = 8
UTENSILIOS = 9
DIVERSOS = 10

LISTA_VAZIA = -1
LISTA_CHEIA = -2
ITEM_EXISTENTE = -3
ITEM_INEXISTENTE = -4

@dataclass
class Produto:
    nome: str | None = None
    tipo: int | None = None
    estoque: int | None = None
    vendido: int | None = None
    custo: float | None = None
    venda: float | None = None

@dataclass
class TipoNo:
    produto: Produto | None = None
    _prox: TipoNo | None = None

class ListaDinamicaEncadeada():
    def __init__(self):
        self.produto: Produto | None = None
        self._nProdutos = 0
        self._opSt = LISTA_VAZIA
        self._inicio: TipoNo | None = None

    def vazia(self) -> bool:
        return self._inicio == None

    def cheia(self) -> bool:
        return False

    def opStatus(self) -> int:
        return self._opSt

    def totalItens(self) -> int:
        return self._nProdutos

    def _buscarProduto(self, nome: str) -> TipoNo:
        if self.vazia():
            self._opSt = ITEM_INEXISTENTE
            return None

        posAnt: TipoNo | None = None
        atual = self._inicio
        achou = False
        fimCurso = False

        while not achou and not fimCurso:
            achou = nome <= atual.produto.nome

            if not achou:
                posAnt = atual
                atual = atual._prox
                fimCurso = atual == None

        if not achou or nome < atual.produto.nome:
            self._opSt = ITEM_INEXISTENTE
        else:
            self._opSt = ITEM_EXISTENTE

        return posAnt

    def inserir(self, produto: Produto) -> bool:
        if self.cheia():
            self._opSt = LISTA_CHEIA
            return False

        posAnt: TipoNo = self._buscarProduto(produto.nome)

        if self._opSt == ITEM_EXISTENTE:
            return False

        posLivre: TipoNo = TipoNo()
        posLivre.produto = deepcopy(produto)

        if posAnt == None:
            posLivre._prox = self._inicio
            self._inicio = posLivre
        else:
            posLivre._prox = posAnt._prox
            posAnt._prox = posLivre

        self._nProdutos += 1

        return True

    def remover(self, nome: str) -> bool:
        posAnt = self._buscarProduto(nome)

        if self._opSt == ITEM_INEXISTENTE:
            self.produto = None
            return False

        if posAnt == None:
            aux = self._inicio
            self._inicio = self._inicio._prox
        else:
            aux = posAnt._prox
            posAnt._prox = posAnt._prox._prox

        self.produto = deepcopy(aux.produto)
        aux._prox = None
        self._nProdutos -= 1

        return True

    def _nomeTipo(self, tipo: int) -> str:
        match tipo:
            case 1: return "Açougue"
            case 2: return "Padaria"
            case 3: return "Frios e Laticínios"
            case 4: return "Higiene Corporal"
            case 5: return "Limpeza da Casa"
            case 6: return "Hortifruti"
            case 7: return "Grãos, Farináceos e Café"
            case 8: return "Bebidas"
            case 9: return "Utensílios"
            case 10: return "Diversos"
            case _: return "Tipo desconhecido"

    def mostrar(self) -> None:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            print("A lista está vazia!")
            return

        pos = self._inicio
        while pos != None:
            produto = pos.produto
            tipo = self._nomeTipo(produto.tipo)

            print(f"Nome: {produto.nome}")
            print(f"Tipo: {tipo}")
            print(f"Quantidade em estoque: {produto.estoque}")
            print(f"Quantidade vendida: {produto.vendido}")
            print(f"Valor de custo: R$ {produto.custo:.2f}")
            print(f"Valor de venda: R$ {produto.venda:.2f}")

            pos = pos._prox

        print()

    def consultar(self, nome: str) -> bool:
        posAnt = self._buscarProduto(nome)

        if self._opSt == ITEM_INEXISTENTE:
            self.produto = None
            return False

        if posAnt == None:
            self.produto = deepcopy(self._inicio.produto)
        else:
            self.produto = deepcopy(posAnt._prox.produto)

        return True   

    def atualizar(self, produto: Produto) -> int:
        if self.vazia():
            self._opSt = LISTA_VAZIA
            return self._opSt

        posAnt = self._buscarProduto(produto.nome)

        if self._opSt == ITEM_INEXISTENTE:
            return self._opSt

        if posAnt == None:
            aux = self._inicio
        else:
            aux = posAnt._prox

        aux.produto.tipo = produto.tipo
        aux.produto.estoque = produto.estoque
        aux.produto.vendido = produto.vendido
        aux.produto.custo = produto.custo
        aux.produto.venda = produto.venda

        return ITEM_EXISTENTE

    def reinicia(self) -> None:
        self.produto = None
        self._nProdutos = 0
        self._opSt = LISTA_VAZIA
        self._inicio = None

    def relatorioEstoqueCompleto(self, tipo: int | None = None) -> None:
        pos = self._inicio

        while pos != None:
            produto = pos.produto

            if tipo == None or produto.tipo == tipo:
                nomeTipo = self._nomeTipo(produto.tipo)

                print(f"Nome: {produto.nome}")
                print(f"Tipo: {nomeTipo}")
                print(f"Quantidade em estoque: {produto.estoque}")
                print(f"Quantidade vendida: {produto.vendido}")
                print(f"Valor de custo: R$ {produto.custo:.2f}")
                print(f"Valor de venda: R$ {produto.venda:.2f}")
                print("-" * 40)

            pos = pos._prox


    def relatorioProdutosEmEstoque(self) -> None:
        pos = self._inicio

        while pos != None:
            produto = pos.produto

            if produto.estoque > 0:
                print(f"Nome: {produto.nome}")
                print(f"Tipo: {self._nomeTipo(produto.tipo)}")
                print(f"Quantidade em estoque: {produto.estoque}")
                print("-" * 40)

            pos = pos._prox

    def relatorioProdutosEsgotados(self) -> None:
        pos = self._inicio

        while pos != None:
            produto = pos.produto

            if produto.estoque == 0:
                print(f"Nome: {produto.nome}")
                print(f"Tipo: {self._nomeTipo(produto.tipo)}")
                print("Produto esgotado!")
                print("-" * 40)

            pos = pos._prox

    
    def relatorioEstoqueBaixo(self, limite: int = 10) -> None:
        pos = self._inicio

        while pos != None:
            produto = pos.produto

            if 0 < produto.estoque < limite:
                print(f"Nome: {produto.nome}")
                print(f"Tipo: {self._nomeTipo(produto.tipo)}")
                print(f"Quantidade em estoque: {produto.estoque}")
                print("-" * 40)

            pos = pos._prox

    
    def relatorioVendas(self) -> None:
        pos = self._inicio

        totalVendido = 0
        totalBruto = 0.0
        totalLiquido = 0.0

        while pos != None:
            produto = pos.produto

            totalVendido += produto.vendido
            totalBruto += produto.vendido * produto.venda
            totalLiquido += produto.vendido * (produto.venda - produto.custo)

            pos = pos._prox

        print(f"Quantidade total vendida: {totalVendido}")
        print(f"Valor total bruto: R$ {totalBruto:.2f}")
        print(f"Valor total líquido: R$ {totalLiquido:.2f}")

    
    def reajustePercentual(self, percentual: float) -> None:
        pos = self._inicio

        while pos != None:
            produto = pos.produto
            produto.venda *= 1 + percentual / 100

            pos = pos._prox


    def reiniciarVendas(self) -> None:
        pos = self._inicio

        while pos != None:
            pos.produto.vendido = 0
            pos = pos._prox


def lerNumero(tipo = int):
    while True:
        try:
            numero = tipo(input("Digite um número: "))

            if numero >= 0:
                return numero

            print("O número não pode ser negativo!")

        except ValueError:
            print("Digite um número válido!")

def lerProduto() -> Produto:
    nome = input("Nome do produto: ").strip()

    while not nome:
        nome = input("Informe um nome válido: ").strip()

    tipo = escolherTipo()

    print("Quantidade em estoque:")
    estoque = lerNumero()

    print("Quantidade vendida:")
    vendido = lerNumero()

    print("Valor de custo:")
    custo = lerNumero(float)

    print("Valor de venda:")
    venda = lerNumero(float)

    return Produto(nome, tipo, estoque, vendido, custo, venda)

def escolherTipo() -> int:
    print("\n===== TIPOS DE PRODUTO =====")
    print("1 - Açougue")
    print("2 - Padaria")
    print("3 - Frios e Laticínios")
    print("4 - Higiene Corporal")
    print("5 - Limpeza da Casa")
    print("6 - Hortifruti")
    print("7 - Grãos, Farináceos e Café")
    print("8 - Bebidas")
    print("9 - Utensílios")
    print("10 - Diversos")

    while True:
        try:
            tipo = int(input("Escolha o tipo (1-10): "))

            if 1 <= tipo <= 10:
                return tipo

            print("Tipo inválido! Escolha entre 1 e 10.")

        except ValueError:
            print("Digite um número válido!")

def main():
    lista = ListaDinamicaEncadeada()

    while True:
        print("\n===== CONTROLE DE ESTOQUE =====")
        print("1 - Inserir produto")
        print("2 - Remover produto")
        print("3 - Atualizar produto")
        print("4 - Relatórios de estoque")
        print("5 - Relatório de vendas")
        print("6 - Reajuste percentual")
        print("7 - Reiniciar vendas")
        print("0 - Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida!")
            continue

        match opcao:
            case 1:
                print("\n===== INSERIR PRODUTO =====")
                produto = lerProduto()

                if lista.inserir(produto):
                    print("Produto inserido com sucesso!")
                else:
                    print("Não foi possível inserir o produto!")

            case 2:
                print("\n===== REMOVER PRODUTO =====")
                nome = input("Nome do produto: ").strip()

                if lista.remover(nome):
                    print("Produto removido com sucesso!")
                else:
                    print("Produto não encontrado!")

            case 3:
                print("\n===== ATUALIZAR PRODUTO =====")
                print("Informe o nome do produto e os novos dados.")
                produto = lerProduto()

                atualizado = lista.atualizar(produto)
                if atualizado == ITEM_EXISTENTE:
                    print("Produto atualizado com sucesso!")
                else:
                    print("Produto não encontrado!")

            case 4:
                while True:
                    print("\n===== RELATÓRIOS DE ESTOQUE =====")
                    print("1 - Completo (todos)")
                    print("2 - Completo (por tipo)")
                    print("3 - Produtos em estoque")
                    print("4 - Produtos esgotados")
                    print("5 - Produtos com estoque baixo")
                    print("0 - Voltar")

                    try:
                        relatorio = int(input("Escolha o relatório: "))
                        print()
                    except ValueError:
                        print("Opção inválida!")
                        continue

                    match relatorio:
                        case 1:
                            lista.relatorioEstoqueCompleto()

                        case 2:
                            tipo = escolherTipo()
                            lista.relatorioEstoqueCompleto(tipo)

                        case 3:
                            lista.relatorioProdutosEmEstoque()

                        case 4:
                            lista.relatorioProdutosEsgotados()

                        case 5:
                            lista.relatorioEstoqueBaixo()

                        case 0:
                            break

                        case _:
                            print("Opção inválida!")

            case 5:
                print("\n===== RELATÓRIO DE VENDAS =====")
                lista.relatorioVendas()

            case 6:
                print("\n===== REAJUSTE PERCENTUAL =====")

                try:
                    percentual = float(input("Percentual de reajuste: ").replace(",", "."))

                    if percentual < -100:
                        print("O reajuste não pode ser inferior a -100%!")
                        continue

                    lista.reajustePercentual(percentual)
                    print("Preços reajustados com sucesso!")

                except ValueError:
                    print("Percentual inválido!")

            case 7:
                print("\n===== REINICIAR VENDAS =====")
                confirmacao = input("Deseja zerar todas as quantidades vendidas? (s/n): ").lower()

                if confirmacao == "s":
                    lista.reiniciarVendas()
                    print("Vendas reiniciadas com sucesso!")
                else:
                    print("Operação cancelada!")

            case 0:
                print("Encerrando...")
                break

            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    main()