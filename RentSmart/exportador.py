"""Geração do arquivo CSV com a projeção de 12 meses."""
import csv
from typing import List

from dinheiro import formatar_csv
from orcamento import LinhaProjecao, Orcamento


class ExportadorCSV:
    """Responsável apenas por gravar a projeção em arquivo CSV.

    Padrão brasileiro: separador ';', vírgula decimal e UTF-8 com BOM,
    para abrir corretamente no Excel.
    """

    CABECALHO = ["Mes", "Aluguel mensal (R$)", "Parcela taxa contratual (R$)",
                 "Total do mes (R$)", "Total acumulado (R$)"]

    def __init__(self, caminho: str = "projecao_12_meses.csv"):
        self.caminho = caminho

    def exportar(self, orcamento: Orcamento) -> str:
        linhas: List[LinhaProjecao] = orcamento.projecao(12)
        with open(self.caminho, "w", newline="", encoding="utf-8-sig") as arq:
            escritor = csv.writer(arq, delimiter=";")
            escritor.writerow(self.CABECALHO)
            for l in linhas:
                escritor.writerow([l.mes, formatar_csv(l.aluguel),
                                   formatar_csv(l.parcela_taxa),
                                   formatar_csv(l.total_mes),
                                   formatar_csv(l.acumulado)])
            total_aluguel = sum(l.aluguel for l in linhas)
            total_taxa = sum(l.parcela_taxa for l in linhas)
            escritor.writerow(["TOTAL", formatar_csv(total_aluguel),
                               formatar_csv(total_taxa),
                               formatar_csv(linhas[-1].acumulado), ""])
        return self.caminho
