"""Funções de leitura e validação de dados digitados pelo usuário."""
from typing import Sequence


def ler_texto(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  Entrada inválida: este campo não pode ficar vazio.")


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        bruto = input(mensagem).strip()
        try:
            valor = int(bruto)
        except ValueError:
            print("  Entrada inválida: digite um número inteiro.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  Valor fora do intervalo: digite de {minimo} a {maximo}.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem + " (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("  Entrada inválida: responda com 's' ou 'n'.")


def ler_opcao(titulo: str, opcoes: Sequence[str]) -> int:
    """Mostra um menu numerado e devolve a posição escolhida (1..n)."""
    print(titulo)
    for i, texto in enumerate(opcoes, start=1):
        print(f"  [{i}] {texto}")
    return ler_inteiro("Escolha: ", 1, len(opcoes))
