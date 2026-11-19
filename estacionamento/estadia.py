from .vagas import Estacionamento, Vaga
from .veiculos import Veiculo


class RegistroEstadia:
    """Associação: conecta um Veiculo a uma Vaga durante uma estadia."""

    def __init__(self, veiculo: Veiculo, vaga: Vaga) -> None:
        self.veiculo = veiculo
        self.vaga = vaga
        self.vaga.ocupar()
        self.encerrada = False
        self.horas: int | None = None
        self.valor_pago: float | None = None

    def encerrar(self, estacionamento: Estacionamento, horas: int) -> float:
        """Dependência: usa o Estacionamento só durante esta chamada."""
        if self.encerrada:
            raise RuntimeError("Esta estadia já foi encerrada.")
        valor = estacionamento.calcular_valor_saida(self.veiculo, horas)
        self.vaga.liberar()
        self.encerrada = True
        self.horas = horas
        self.valor_pago = valor
        return valor


class GeradorRecibo:
    """Dependência: usa RegistroEstadia pontualmente apenas para gerar texto."""

    def gerar(self, registro: RegistroEstadia) -> str:
        if not registro.encerrada or registro.valor_pago is None:
            raise RuntimeError("Não é possível gerar recibo de estadia em aberto.")
        return (
            f"=== RECIBO ===\n"
            f"Vaga: {registro.vaga.codigo}\n"
            f"Veículo: {registro.veiculo}\n"
            f"Horas: {registro.horas}h\n"
            f"Total: R$ {registro.valor_pago:.2f}"
        )
