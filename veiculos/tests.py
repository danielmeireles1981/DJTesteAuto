from django.test import TestCase
from .models import Autobot
from django.urls import reverse
from .forms import AutobotForm

class AutobotModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n=== TESTE: Modelo Autobot ===")

    def setUp(self):
        self.autobot = Autobot.objects.create(
            nome="Optimus Prime",
            tipo="Caminhão",
            poder=100,
            frase_batalha="Autobots, transformar e avançar!"
        )

    def test_autobot_criado(self):
        autobot = Autobot.objects.get(nome="Optimus Prime")
        self.assertEqual(
            autobot.tipo, "Caminhão",
            "ERRO: O tipo do Autobot 'Optimus Prime' não está correto. Esperado: 'Caminhão', Encontrado: '%s'. Certifique-se que o tipo está sendo salvo corretamente no modelo." % autobot.tipo
        )
        self.assertEqual(
            autobot.poder, 100,
            "ERRO: O poder de 'Optimus Prime' deveria ser 100, mas está %s. Verifique a criação e o salvamento do objeto." % autobot.poder
        )
        self.assertIn(
            "Autobots", autobot.frase_batalha,
            "ERRO: A frase de batalha de 'Optimus Prime' deveria conter 'Autobots'. Frase atual: '%s'. Verifique o atributo 'frase_batalha'." % autobot.frase_batalha
        )

class AutobotViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n=== TESTE: Views de Cadastro e Listagem dos Autobots ===")

    def test_cadastrar_autobot(self):
        response = self.client.post(reverse('cadastrar_autobot'), {
            'nome': 'Bumblebee',
            'tipo': 'Carro',
            'poder': 80,
            'frase_batalha': "Bee pronto para missão!"
        })
        self.assertEqual(
            response.status_code, 302,
            "ERRO: Ao cadastrar 'Bumblebee', o sistema não fez o redirecionamento esperado (status 302). Isso indica que o cadastro não está funcionando corretamente."
        )
        self.assertTrue(
            Autobot.objects.filter(nome='Bumblebee').exists(),
            "ERRO: O Autobot 'Bumblebee' não foi encontrado no banco de dados após o cadastro. Verifique a view de cadastro."
        )

    def test_listar_autobots(self):
        Autobot.objects.create(
            nome="Ratchet", tipo="Ambulância", poder=70,
            frase_batalha="Vamos consertar o que puder!"
        )
        response = self.client.get(reverse('listar_autobots'))
        self.assertContains(
            response, "Ratchet",
            "ERRO: O Autobot 'Ratchet' não apareceu na listagem. Verifique se a view e o template estão exibindo todos os Autobots cadastrados."
        )

class AutobotFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n=== TESTE: Formulários dos Autobots ===")

    def test_form_valido(self):
        form_data = {
            'nome': 'Ironhide',
            'tipo': 'Caminhão',
            'poder': 85,
            'frase_batalha': 'Ninguém mexe com os Autobots!'
        }
        form = AutobotForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "ERRO: O formulário deveria ser válido para 'Ironhide', mas não foi. Verifique as regras de validação do ModelForm."
        )

    def test_form_invalido(self):
        form_data = {
            'nome': '',  # Nome obrigatório
            'tipo': 'Moto',
            'poder': '',
            'frase_batalha': ''
        }
        form = AutobotForm(data=form_data)
        self.assertFalse(
            form.is_valid(),
            "ERRO: O formulário deveria ser inválido (nome, poder e frase_batalha obrigatórios), mas foi considerado válido. Revise as validações obrigatórias do formulário."
        )

class AutobotIntegracaoTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n=== TESTE: Integração (Cadastro e Listagem Completa) ===")

    def test_fluxo_completo(self):
        # Cadastro
        response = self.client.post(reverse('cadastrar_autobot'), {
            'nome': 'Jazz',
            'tipo': 'Carro Esportivo',
            'poder': 77,
            'frase_batalha': 'A música é minha arma secreta!'
        })
        self.assertEqual(
            response.status_code, 302,
            "ERRO: Após cadastrar 'Jazz', não houve redirecionamento (status 302). O cadastro pode estar falhando."
        )
        # Listagem
        response = self.client.get(reverse('listar_autobots'))
        self.assertContains(
            response, 'Jazz',
            "ERRO: 'Jazz' não apareceu na listagem após o cadastro. Verifique se o cadastro e a listagem estão integrados corretamente."
        )
        self.assertContains(
            response, 'Carro Esportivo',
            "ERRO: O tipo 'Carro Esportivo' de 'Jazz' não apareceu na listagem. Confira o template da listagem."
        )
