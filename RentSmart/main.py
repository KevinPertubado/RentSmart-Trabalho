"""RentSmart - Sistema de orçamento de locação da R.M Imóveis."""
from dinheiro import formatar_brl
from entrada import ler_inteiro, ler_opcao, ler_sim_nao, ler_texto
from exportador import ExportadorCSV
from imoveis import Apartamento, Casa, Estudio, Imovel
from orcamento import Cliente, Orcamento, TaxaContratual

LARGURA = 60


def coletar_imovel() -> Imovel:
    """Pergunta ao usuário as características e devolve o objeto de imóvel."""
    tipo = ler_opcao("\nTipo de imóvel:",
                     ["Apartamento", "Casa", "Estúdio"])
    if tipo == 3:
        vagas = ler_inteiro(
            "Quantas vagas de estacionamento (0 = nenhuma)? ", 0, 10)
        return Estudio(vagas)

    quartos = ler_opcao("\nQuantidade de quartos:", ["1 quarto", "2 quartos"])
    garagem = ler_sim_nao("Deseja vaga de garagem?")
    if tipo == 1:
        tem_criancas = ler_sim_nao("Possui crianças?")
        return Apartamento(quartos, garagem, tem_criancas)
    return Casa(quartos, garagem)


def exibir_orcamento(orc: Orcamento) -> None:
    linha = "=" * LARGURA

    def item(texto: str, valor: str) -> None:
        print(f"  {texto:<{LARGURA - 20}}{valor:>16}")

    print(f"\n{linha}\n{'RESUMO DO ORÇAMENTO - R.M IMÓVEIS':^{LARGURA}}\n{linha}")
    print(f"  Cliente: {orc.cliente.nome}")
    print(f"  Imóvel : {orc.imovel.descricao()}")
    print("-" * LARGURA)
    print("  ALUGUEL MENSAL")
    item("Aluguel-base", formatar_brl(orc.imovel.aluguel_base))
    for adicional in orc.adicionais():
        item("+ " + adicional.descricao, formatar_brl(adicional.valor))
    item("Subtotal", formatar_brl(orc.subtotal()))
    desconto = orc.desconto()
    if desconto:
        item("- " + desconto.descricao, formatar_brl(desconto.valor))
    item("VALOR MENSAL DO ALUGUEL", formatar_brl(orc.aluguel_mensal()))
    print("-" * LARGURA)
    print("  TAXA CONTRATUAL (cobrada à parte, não é aluguel)")
    item("Valor total da taxa", formatar_brl(orc.taxa.valor))
    item("Parcelamento escolhido",
         f"{orc.taxa.parcelas}x de {formatar_brl(orc.taxa.valor_parcela(1))}")
    print("-" * LARGURA)
    print("  PRIMEIROS 12 MESES")
    item("Total previsto (aluguéis + taxa)",
         formatar_brl(orc.total_primeiro_ano()))
    print(linha)


def gerar_orcamento() -> None:
    print("\n--- NOVO ORÇAMENTO ---")
    cliente = Cliente(ler_texto("Nome do cliente: "))
    imovel = coletar_imovel()
    parcelas = ler_inteiro(
        "\nTaxa contratual de R$ 2.000,00: em quantas parcelas (1 a 5)? ", 1, 5)
    orcamento = Orcamento(cliente, imovel, TaxaContratual(parcelas))

    exibir_orcamento(orcamento)
    caminho = ExportadorCSV("projecao_12_meses.csv").exportar(orcamento)
    print(f"\nArquivo CSV com a projeção de 12 meses gerado: {caminho}")


def main() -> None:
    print("=" * LARGURA)
    print(f"{'RentSmart - R.M Imóveis':^{LARGURA}}")
    print("=" * LARGURA)
    while True:
        gerar_orcamento()
        if not ler_sim_nao("\nDeseja fazer outro orçamento?"):
            print("Obrigado por usar o RentSmart!")
            break


if __name__ == "__main__":
    main()
