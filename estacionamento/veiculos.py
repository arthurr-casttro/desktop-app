from abc import ABC, abstractmethod


class Veiculo(ABC):
    """Classe base abstrata (herança). Define o contrato de todo veículo."""

    def __init__(self, placa: str) -> None:
        placa_limpa = placa.strip().upper()
        if not placa_limpa:
            raise ValueError("Placa não pode ser vazia.")
        self._placa = placa_limpa

    @property
    def placa(self) -> str:
        return self._placa

    @abstractmethod
    def tipo(self) -> str:
        """Retorna o nome do tipo de veículo."""

    @abstractmethod
    def valor_hora(self) -> float:
        """Retorna o valor cobrado por hora para este tipo de veículo."""

    def calcular_tarifa(self, horas: int) -> float:
        """Calcula o valor da estadia para uma quantidade inteira de horas (>= 1).

        Template method: a regra geral fica aqui e cada subclasse fornece
        seu `valor_hora()` ou sobrescreve este método (polimorfismo).
        """
        if horas <= 0:
            raise ValueError("Horas deve ser maior que zero.")
        return round(horas * self.valor_hora(), 2)

    def __str__(self) -> str:
        return f"{self.tipo()} ({self.placa})"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.placa!r})"


class Carro(Veiculo):
    VALOR_HORA = 10.0

    def tipo(self) -> str:
        return "Carro"

    def valor_hora(self) -> float:
        return self.VALOR_HORA


class Moto(Veiculo):
    VALOR_HORA = 5.0

    def tipo(self) -> str:
        return "Moto"

    def valor_hora(self) -> float:
        return self.VALOR_HORA


class Caminhonete(Veiculo):
    VALOR_HORA = 15.0
    TAXA_FIXA = 5.0

    def tipo(self) -> str:
        return "Caminhonete"

    def valor_hora(self) -> float:
        return self.VALOR_HORA

    def calcular_tarifa(self, horas: int) -> float:
        # Sobrescrita: reaproveita a regra da classe base e soma uma taxa fixa
        return round(super().calcular_tarifa(horas) + self.TAXA_FIXA, 2)
