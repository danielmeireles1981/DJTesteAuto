from django.core.management.base import BaseCommand
import io
from django.test.runner import DiscoverRunner
import re

class Command(BaseCommand):
    help = "Roda os testes dos Autobots e exibe o log formatado"

    def add_arguments(self, parser):
        parser.add_argument(
            '--app', type=str, default='veiculos',
            help='Nome do app Django para rodar os testes (padrão: veiculos)'
        )

    def handle(self, *args, **options):
        app_name = options['app']
        stream = io.StringIO()
        runner = DiscoverRunner(verbosity=2, stream=stream)

        ascii_header = (
            "\n" + "=" * 65 +
            "\n[ RELATÓRIO DE TESTES DOS AUTOBOTS ]\n" +
            "=" * 65 +
            "\nCada teste verifica uma missão da equipe Autobot.\n" +
            "-" * 65 +
            "\nResultados:\n" +
            "  ok     -> Missão concluída\n" +
            "  FAIL   -> Missão falhou (veja o motivo abaixo)\n" +
            "  ERROR  -> Erro inesperado durante a missão\n" +
            "-" * 65 + "\n"
        )
        print(ascii_header)

        # Rodando os testes
        failures = runner.run_tests([app_name])
        stream.flush()
        log = stream.getvalue()
        print(log)

        print("-" * 65)
        print("RESUMO DA MISSÃO:")
        print("-" * 65)

        # Extrair mensagens dos FAILS e ERRORS do log (usando regex simples)
        failed_sections = re.findall(
            r'(FAIL: .+?)(?=(?:FAIL: |ERROR: |\Z))', log, flags=re.DOTALL)
        error_sections = re.findall(
            r'(ERROR: .+?)(?=(?:FAIL: |ERROR: |\Z))', log, flags=re.DOTALL)

        if failures:
            print("X MISSÃO DOS AUTOBOTS FALHOU!")
            print("Confira abaixo as falhas detalhadas para correção:")
            print("-" * 65)
            # Exibe motivos de todas as falhas
            for fail in failed_sections:
                print("\n--- FALHA DETECTADA ---")
                print(fail.strip())
            for error in error_sections:
                print("\n--- ERRO DETECTADO ---")
                print(error.strip())
            print("-" * 65)
            print("Consulte acima os motivos e corrija antes de rodar novamente.")
        else:
            print("V MISSÃO DOS AUTOBOTS CONCLUÍDA COM SUCESSO!")
            print("Todas as missões foram cumpridas sem falhas. Equipe operacional.")

        print("=" * 65)
