"""Hierarquia de imóveis da R.M Imóveis.

Cada tipo de imóvel conhece as próprias regras comerciais (aluguel-base,
adicionais e descontos). Assim, o restante do sistema não precisa usar
vários "if tipo == ..." espalhados: basta chamar os métodos do objeto
(polimorfismo).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

from dinheiro import dinheiro


@dataclass(frozen=True)
class ItemOrcamento:
    """Uma linha do orçamento: descrição + valor mensal."""
    descricao: str
    valor: Decimal


class Imovel(ABC):
    """Classe abstrata: define o que todo imóvel precisa oferecer."""

    nome_tipo: str = ""
    aluguel_base: Decimal = Decimal("0")

    def __init__(self, quartos: int = 1):
        self.quartos = quartos

    @abstractmethod
    def adicionais(self) -> List[ItemOrcamento]:
        """Lista de acréscimos mensais (quartos extras, vagas etc.)."""

    def desconto(self, subtotal: Decimal) -> Optional[ItemOrcamento]:
        """Desconto aplicável sobre o subtotal. Por padrão, não há desconto."""
        return None

    def descricao(self) -> str:
        return self.nome_tipo

    def __str__(self) -> str:
        return self.descricao()


class ImovelResidencial(Imovel):
    """Casas e apartamentos: adicional por 2º quarto e vaga de garagem."""

    adicional_dois_quartos: Decimal = Decimal("0")
    valor_garagem: Decimal = Decimal("300.00")
    quartos_permitidos = (1, 2)

    def __init__(self, quartos: int = 1, possui_garagem: bool = False):
        if quartos not in self.quartos_permitidos:
            raise ValueError("Quantidade de quartos inválida (use 1 ou 2).")
        super().__init__(quartos)
        self.possui_garagem = possui_garagem

    def adicionais(self) -> List[ItemOrcamento]:
        itens: List[ItemOrcamento] = []
        if self.quartos == 2:
            itens.append(ItemOrcamento("Adicional de 2º quarto",
                                       dinheiro(self.adicional_dois_quartos)))
        if self.possui_garagem:
            itens.append(ItemOrcamento("Vaga de garagem",
                                       dinheiro(self.valor_garagem)))
        return itens

    def descricao(self) -> str:
        plural = "quarto" if self.quartos == 1 else "quartos"
        return f"{self.nome_tipo} de {self.quartos} {plural}"


class Apartamento(ImovelResidencial):
    nome_tipo = "Apartamento"
    aluguel_base = Decimal("700.00")
    adicional_dois_quartos = Decimal("200.00")
    percentual_desconto_sem_criancas = Decimal("0.05")

    def __init__(self, quartos: int = 1, possui_garagem: bool = False,
                 tem_criancas: bool = True):
        super().__init__(quartos, possui_garagem)
        self.tem_criancas = tem_criancas

    def desconto(self, subtotal: Decimal) -> Optional[ItemOrcamento]:
        """5% de desconto para quem não possui crianças (após os adicionais)."""
        if self.tem_criancas:
            return None
        valor = dinheiro(subtotal * self.percentual_desconto_sem_criancas)
        return ItemOrcamento("Desconto de 5% (sem crianças)", valor)


class Casa(ImovelResidencial):
    nome_tipo = "Casa"
    aluguel_base = Decimal("900.00")
    adicional_dois_quartos = Decimal("250.00")


class Estudio(Imovel):
    """Estúdio: estacionamento em pacote de 2 vagas + vagas adicionais."""

    nome_tipo = "Estúdio"
    aluguel_base = Decimal("1200.00")
    pacote_vagas = 2
    valor_pacote = Decimal("250.00")
    valor_vaga_adicional = Decimal("60.00")

    def __init__(self, vagas: int = 0):
        if vagas < 0:
            raise ValueError("A quantidade de vagas não pode ser negativa.")
        super().__init__(quartos=1)
        self.vagas = vagas

    def adicionais(self) -> List[ItemOrcamento]:
        if self.vagas == 0:
            return []
        itens = [ItemOrcamento(
            f"Estacionamento - pacote inicial de {self.pacote_vagas} vagas",
            dinheiro(self.valor_pacote))]
        extras = self.vagas - self.pacote_vagas
        if extras > 0:
            total_extras = self.valor_vaga_adicional * extras
            itens.append(ItemOrcamento(
                f"Vagas adicionais ({extras} x "
                f"R$ {self.valor_vaga_adicional:.2f})".replace(".", ","),
                dinheiro(total_extras)))
        return itens
