# Roteiro do vídeo pitch (até 4 minutos) - RentSmart

Grave a tela (OBS, Xbox Game Bar `Win+G`, ou Meet/Zoom compartilhando a tela) e publique no YouTube como **não listado**.
Deixe abertos antes de gravar: o PDF (fluxogramas e diagrama de classes), o VS Code com a pasta do projeto, o terminal e a pasta onde o CSV será gerado.

| Tempo | O que mostrar | O que falar (sugestão) |
|---|---|---|
| 0:00-0:25 | Slide/PDF: capa | "Olá, sou Kevin Morais, RA 251009. Este é o RentSmart, sistema da R.M Imóveis que calcula orçamentos de locação. Hoje o cálculo é manual e gera demora e erros em adicionais e descontos. O sistema automatiza tudo e gera uma projeção de 12 meses em CSV." |
| 0:25-1:05 | PDF: fluxogramas (partes 1 e 2) | "O fluxo começa lendo e validando os dados: nome, tipo de imóvel, quartos, garagem, crianças, vagas e parcelas. Depois monta os objetos, soma aluguel-base e adicionais, aplica 5% de desconto só se for apartamento sem crianças, calcula a taxa de R$ 2.000 em parcelas, projeta 12 meses, mostra o resumo e grava o CSV. No final pergunta se há outro orçamento." |
| 1:05-1:50 | PDF: diagrama de classes + VS Code (imoveis.py) | "Imovel é uma classe abstrata. ImovelResidencial guarda o que casa e apartamento têm em comum: 2º quarto e garagem. Apartamento e Casa herdam dela, e só o Apartamento sobrescreve o método desconto. Estudio herda direto de Imovel porque tem regra própria de vagas. Orcamento reúne Cliente, Imovel e TaxaContratual. ExportadorCSV só cuida de gravar o arquivo." |
| 1:50-2:30 | VS Code: `imoveis.py` (Apartamento.desconto, Estudio.adicionais) e `orcamento.py` (aluguel_mensal, projecao) | "Aqui o polimorfismo: o Orcamento chama imovel.adicionais() e imovel.desconto() sem checar o tipo. Uso Decimal para dinheiro, e a última parcela da taxa ajusta os centavos para a soma fechar R$ 2.000." |
| 2:30-3:20 | Terminal: `python main.py` | Digite: nome "Maria Silva", Apartamento, 2 quartos, garagem **s**, crianças **n**, 3 parcelas. "Vejam: aluguel-base 700, mais 200 do segundo quarto, mais 300 da garagem, subtotal 1.200, desconto de 5% = 60, aluguel mensal R$ 1.140. A taxa aparece separada, 3x de R$ 666,67." (Se der tempo, digite uma letra onde pede número para mostrar a validação.) |
| 3:20-3:40 | Abrir `projecao_12_meses.csv` (Excel) | "Este é o CSV: meses 1 a 3 têm aluguel mais parcela da taxa; do mês 4 ao 12, só o aluguel. Total em 12 meses: R$ 15.680,00." |
| 3:40-4:00 | VS Code: testes (`python -m unittest`) ou árvore de arquivos | "A POO deixou o código organizado: cada regra mora na classe certa, sem repetição, e um novo tipo de imóvel é só uma nova subclasse. Obrigado!" |

Dicas: ensaie uma vez com cronômetro; aumente o zoom do VS Code e do terminal (Ctrl +); confira o link do YouTube em janela anônima antes de enviar.
