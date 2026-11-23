# RentSmart - Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação em **Python** (somente biblioteca padrão) que recebe as características
da locação, aplica as regras comerciais da R.M Imóveis, mostra um resumo
detalhado do orçamento e gera um **CSV com a projeção dos 12 primeiros meses**.

Projeto da disciplina *Algorithmic Thinking & Introduction to Object-Oriented Programming*.

- **Autor:** Kevin Morais Pereira Silva - RA 251009 - UniFecaf

## Requisitos

- Python 3.9 ou superior (testado no 3.12). Não precisa instalar nenhuma biblioteca.

## Como executar

```bash
git clone <LINK-DO-SEU-REPOSITORIO>
cd RentSmart
python main.py        # no Linux/macOS, se necessário: python3 main.py
```

O programa pergunta: nome do cliente, tipo de imóvel (apartamento, casa ou estúdio),
quartos, garagem/vagas, se há crianças (apartamentos) e em quantas parcelas
(1 a 5) a taxa contratual será paga. Entradas inválidas são recusadas e a
pergunta é repetida.

Ao final, é exibido o orçamento e criado o arquivo **`projecao_12_meses.csv`**
na pasta em que o programa foi executado.

## Como rodar os testes

```bash
python -m unittest -v
```

## Regras de negócio implementadas

| Item | Regra |
|---|---|
| Aluguel-base | Apartamento 1 quarto R$ 700 / Casa 1 quarto R$ 900 / Estúdio R$ 1.200 |
| 2º quarto | Apartamento +R$ 200 / Casa +R$ 250 |
| Garagem (casa e apto) | +R$ 300 por mês (1 vaga) |
| Estúdio | Pacote de 2 vagas R$ 250; vaga adicional R$ 60 cada |
| Desconto | Apartamento sem crianças: 5% sobre o aluguel **após** os adicionais |
| Taxa contratual | R$ 2.000 em até 5 parcelas, **apresentada separada do aluguel** |

**Premissa adotada (estúdio):** o cliente informa quantas vagas deseja. 0 = sem
estacionamento; 1 ou 2 = pacote inicial de R$ 250; acima de 2 = R$ 250 + R$ 60
por vaga adicional.

## Estrutura do projeto

```
RentSmart/
├── main.py            # interface de terminal (menu, resumo, fluxo principal)
├── imoveis.py         # Imovel (abstrata), ImovelResidencial, Apartamento, Casa, Estudio, ItemOrcamento
├── orcamento.py       # Cliente, TaxaContratual, LinhaProjecao, Orcamento
├── exportador.py      # ExportadorCSV
├── entrada.py         # leitura e validação das entradas
├── dinheiro.py        # Decimal, arredondamento e formatação em R$
├── test_rentsmart.py  # testes automatizados das regras
└── README.md
```

## Arquivo CSV gerado

Separador `;`, vírgula decimal e UTF-8 (abre direto no Excel em português).
Colunas: `Mes; Aluguel mensal; Parcela taxa contratual; Total do mes; Total acumulado`,
com 12 linhas e uma linha final de TOTAL.

## Exemplo

Apartamento de 2 quartos, com garagem, sem crianças, taxa em 3x:
(700 + 200 + 300) = R$ 1.200,00 - 5% = **R$ 1.140,00/mês**; taxa 3x de R$ 666,67
(última parcela R$ 666,66); total dos 12 meses: **R$ 15.680,00**.
