"""Classes do processo comercial: cliente, taxa contratual, orçamento."""
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

from dinheiro import dinheiro
from imoveis import Imovel, ItemOrcamento


@dataclass(frozen=True)
class Cliente:
    nome: str

    def __post_init__(self):
        if not self.nome.strip():
            raise ValueError("O nome do cliente não pode ser vazio.")


class TaxaContratual:
    """Taxa única do contrato, paga em parcelas (separada do aluguel)."""

    VALOR = Decimal("2000.00")
    MAX_PARCELAS = 5

    def __init__(self, parcelas: int = 1):
        if not 1 <= parcelas <= self.MAX_PARCELAS:
            raise ValueError(
                f"O parcelamento deve ser de 1 a {self.MAX_PARCELAS} vezes.")
        self.valor = dinheiro(self.VALOR)
        self.parcelas = parcelas

    def valor_parcela(self, numero: int) -> Decimal:
        """Valor da parcela `numero` (1..n). Fora do prazo, retorna zero.

        A última parcela absorve eventuais centavos de diferença
        (ex.: 2000 / 3 = 666,67 + 666,67 + 666,66).
        """
        if not 1 <= numero <= self.parcelas:
            return Decimal("0.00")
        base = dinheiro(self.valor / self.parcelas)
        if numero < self.parcelas:
            return base
        return self.valor - base * (self.parcelas - 1)

    def __str__(self) -> str:
        return f"{self.parcelas}x"


@dataclass(frozen=True)
class LinhaProjecao:
    """Uma linha da projeção mensal (um mês do contrato)."""
    mes: int
    aluguel: Decimal
    parcela_taxa: Decimal
    total_mes: Decimal
    acumulado: Decimal


class Orcamento:
    """Reúne cliente, imóvel e taxa e calcula todos os valores."""

    def __init__(self, cliente: Cliente, imovel: Imovel, taxa: TaxaContratual):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    # ---- cálculos do aluguel mensal -------------------------------------
    def adicionais(self) -> List[ItemOrcamento]:
        return self.imovel.adicionais()

    def subtotal(self) -> Decimal:
        """Aluguel-base + adicionais (antes de descontos)."""
        total = dinheiro(self.imovel.aluguel_base)
        for item in self.adicionais():
            total += item.valor
        return total

    def desconto(self) -> Optional[ItemOrcamento]:
        return self.imovel.desconto(self.subtotal())

    def aluguel_mensal(self) -> Decimal:
        desconto = self.desconto()
        return self.subtotal() - (desconto.valor if desconto else Decimal("0"))

    # ---- projeção --------------------------------------------------------
    def projecao(self, meses: int = 12) -> List[LinhaProjecao]:
        linhas: List[LinhaProjecao] = []
        acumulado = Decimal("0.00")
        for mes in range(1, meses + 1):
            parcela = self.taxa.valor_parcela(mes)
            total = self.aluguel_mensal() + parcela
            acumulado += total
            linhas.append(LinhaProjecao(mes, self.aluguel_mensal(),
                                        parcela, total, acumulado))
        return linhas

    def total_primeiro_ano(self) -> Decimal:
        return self.projecao()[-1].acumulado
