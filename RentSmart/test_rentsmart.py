"""Testes automatizados das regras de negócio (python -m unittest)."""
import unittest
from decimal import Decimal as D

from imoveis import Apartamento, Casa, Estudio
from orcamento import Cliente, Orcamento, TaxaContratual


def orc(imovel, parcelas=1):
    return Orcamento(Cliente("Teste"), imovel, TaxaContratual(parcelas))


class TestAluguel(unittest.TestCase):
    def test_bases(self):
        self.assertEqual(orc(Apartamento()).aluguel_mensal(), D("700.00"))
        self.assertEqual(orc(Casa()).aluguel_mensal(), D("900.00"))
        self.assertEqual(orc(Estudio()).aluguel_mensal(), D("1200.00"))

    def test_dois_quartos(self):
        self.assertEqual(orc(Apartamento(2)).aluguel_mensal(), D("900.00"))
        self.assertEqual(orc(Casa(2)).aluguel_mensal(), D("1150.00"))

    def test_garagem(self):
        self.assertEqual(orc(Casa(1, True)).aluguel_mensal(), D("1200.00"))
        self.assertEqual(orc(Apartamento(1, True)).aluguel_mensal(), D("1000.00"))

    def test_estudio_vagas(self):
        self.assertEqual(orc(Estudio(2)).aluguel_mensal(), D("1450.00"))
        self.assertEqual(orc(Estudio(4)).aluguel_mensal(), D("1570.00"))

    def test_desconto_sem_criancas_apos_adicionais(self):
        # (700 + 200 + 300) * 0,95 = 1140,00
        apto = Apartamento(2, True, tem_criancas=False)
        self.assertEqual(orc(apto).aluguel_mensal(), D("1140.00"))

    def test_sem_desconto_com_criancas(self):
        apto = Apartamento(2, True, tem_criancas=True)
        self.assertEqual(orc(apto).aluguel_mensal(), D("1200.00"))

    def test_casa_nao_tem_desconto(self):
        self.assertIsNone(orc(Casa(1, True)).desconto())


class TestTaxaEProjecao(unittest.TestCase):
    def test_parcelas_somam_taxa(self):
        for n in range(1, 6):
            t = TaxaContratual(n)
            self.assertEqual(sum(t.valor_parcela(i) for i in range(1, n + 1)),
                             D("2000.00"))

    def test_parcelamento_invalido(self):
        with self.assertRaises(ValueError):
            TaxaContratual(6)
        with self.assertRaises(ValueError):
            TaxaContratual(0)

    def test_projecao_12_meses(self):
        o = orc(Casa(1), parcelas=5)   # 900 + 5 x 400
        linhas = o.projecao()
        self.assertEqual(len(linhas), 12)
        self.assertEqual(linhas[0].total_mes, D("1300.00"))
        self.assertEqual(linhas[5].total_mes, D("900.00"))
        self.assertEqual(o.total_primeiro_ano(), D("12800.00"))

    def test_validacoes(self):
        with self.assertRaises(ValueError):
            Casa(3)
        with self.assertRaises(ValueError):
            Estudio(-1)
        with self.assertRaises(ValueError):
            Cliente("   ")


if __name__ == "__main__":
    unittest.main()
