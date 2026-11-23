"""Funções utilitárias para trabalhar com valores monetários.

Usamos Decimal (e não float) para evitar erros de arredondamento
em cálculos financeiros, como 5% de desconto ou divisão em parcelas.
"""
from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def dinheiro(valor) -> Decimal:
    """Converte para Decimal com 2 casas decimais (arredondamento comercial)."""
    return Decimal(str(valor)).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def formatar_brl(valor: Decimal) -> str:
    """Formata um valor no padrão brasileiro: R$ 1.234,56."""
    texto = f"{dinheiro(valor):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_csv(valor: Decimal) -> str:
    """Formata para CSV brasileiro (vírgula decimal, sem símbolo): 1234,56."""
    return f"{dinheiro(valor):.2f}".replace(".", ",")
