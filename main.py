from typing import Callable

from estacionamento import (
    Caminhonete,
    Carro,
    Estacionamento,
    GeradorRecibo,
    Moto,
    Veiculo,
)

TIPOS_VEICULO: dict[str, type[Veiculo]] = {
    "1": Carro,
    "2": Moto,
    "3": Caminhonete,
}


class MenuEstacionamento:
    """Interface de terminal.

    Associação: mantém uma referência ao Estacionamento durante toda a execução.
    Dependência: usa GeradorRecibo apenas no momento de imprimir o recibo.
    """

    def __init__(
        self,
        estacionamento: Estacionamento,
        entrada: Callable[[str], str] = input,
        saida: Callable[[str], None] = print,
    ) -> None:
        self.estacionamento = estacionamento
        self._input = entrada
        self._print = saida

    def executar(self) -> None:
        acoes = {
            "1": self.registrar_entrada,
            "2": self.registrar_saida,
            "3": self.listar_vagas,
            "4": self.listar_estacionados,
        }
        while True:
            self._print(
                f"\n=== {self.estacionamento.nome} "
                f"({len(self.estacionamento.vagas_livres())}/"
                f"{self.estacionamento.total_vagas} vagas livres) ===\n"
                "1) Registrar entrada\n"
                "2) Registrar saída\n"
                "3) Listar vagas\n"
                "4) Listar veículos estacionados\n"
                "0) Sair"
            )
            opcao = self._input("Opção: ").strip().lstrip("﻿")
            if opcao == "0":
                self._print("Até logo!")
                return
            acao = acoes.get(opcao)
            if acao is None:
                self._print("Opção inválida.")
                continue
            try:
                acao()
            except (ValueError, RuntimeError) as erro:
                self._print(f"Erro: {erro}")

    def registrar_entrada(self) -> None:
        tipo = self._input("Tipo (1=Carro, 2=Moto, 3=Caminhonete): ").strip()
        classe = TIPOS_VEICULO.get(tipo)
        if classe is None:
            raise ValueError("Tipo de veículo inválido.")
        veiculo = classe(self._input("Placa: "))
        registro = self.estacionamento.registrar_entrada(veiculo)
        self._print(f"{veiculo} estacionado na vaga {registro.vaga.codigo}.")

    def registrar_saida(self) -> None:
        placa = self._input("Placa: ")
        texto_horas = self._input("Horas de permanência: ").strip()
        if not texto_horas.isdigit():
            raise ValueError("Informe um número inteiro de horas.")
        registro = self.estacionamento.registrar_saida(placa, int(texto_horas))
        self._print(GeradorRecibo().gerar(registro))

    def listar_vagas(self) -> None:
        for vaga in self.estacionamento.vagas:
            self._print(str(vaga))

    def listar_estacionados(self) -> None:
        estadias = self.estacionamento.estadias_ativas()
        if not estadias:
            self._print("Nenhum veículo estacionado.")
        for registro in estadias:
            self._print(f"{registro.vaga.codigo}: {registro.veiculo}")


def main() -> None:
    try:
        MenuEstacionamento(Estacionamento("Estacionamento Central", 5)).executar()
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrado.")


if __name__ == "__main__":
    main()
