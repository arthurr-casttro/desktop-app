from __future__ import annotations

from typing import TYPE_CHECKING

from .veiculos import Veiculo

if TYPE_CHECKING:
    from .estadia import RegistroEstadia


class Vaga:
    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        self._ocupada = False

    @property
    def ocupada(self) -> bool:
        return self._ocupada

    def ocupar(self) -> None:
        if self._ocupada:
            raise RuntimeError(f"Vaga {self.codigo} já está ocupada.")
        self._ocupada = True

    def liberar(self) -> None:
        if not self._ocupada:
            raise RuntimeError(f"Vaga {self.codigo} já está livre.")
        self._ocupada = False

    def __str__(self) -> str:
        return f"{self.codigo} [{'ocupada' if self._ocupada else 'livre'}]"

    def __repr__(self) -> str:
        return f"Vaga({self.codigo!r}, ocupada={self._ocupada})"


class Estacionamento:
    """Composição com Vaga (cria e gerencia suas próprias vagas) e
    agregação com RegistroEstadia (controla as estadias em andamento)."""

    def __init__(self, nome: str, quantidade_vagas: int) -> None:
        if quantidade_vagas <= 0:
            raise ValueError("Quantidade de vagas deve ser maior que zero.")
        self.nome = nome
        self._vagas: list[Vaga] = [
            Vaga(f"V{i + 1:02d}") for i in range(quantidade_vagas)
        ]
        self._estadias_ativas: dict[str, RegistroEstadia] = {}

    @property
    def total_vagas(self) -> int:
        return len(self._vagas)

    @property
    def vagas(self) -> list[Vaga]:
        return list(self._vagas)

    def vagas_livres(self) -> list[Vaga]:
        return [v for v in self._vagas if not v.ocupada]

    def buscar_vaga_livre(self) -> Vaga:
        livres = self.vagas_livres()
        if not livres:
            raise RuntimeError("Estacionamento lotado: nenhuma vaga disponível.")
        return livres[0]

    def calcular_valor_saida(self, veiculo: Veiculo, horas: int) -> float:
        # Polimorfismo: delega ao próprio veículo sem checar classe concreta
        return veiculo.calcular_tarifa(horas)

    def registrar_entrada(self, veiculo: Veiculo) -> RegistroEstadia:
        from .estadia import RegistroEstadia

        if veiculo.placa in self._estadias_ativas:
            raise RuntimeError(f"Veículo {veiculo.placa} já está estacionado.")
        registro = RegistroEstadia(veiculo, self.buscar_vaga_livre())
        self._estadias_ativas[veiculo.placa] = registro
        return registro

    def buscar_estadia(self, placa: str) -> RegistroEstadia:
        chave = placa.strip().upper()
        try:
            return self._estadias_ativas[chave]
        except KeyError:
            raise RuntimeError(f"Nenhum veículo com placa {chave} estacionado.") from None

    def registrar_saida(self, placa: str, horas: int) -> RegistroEstadia:
        registro = self.buscar_estadia(placa)
        registro.encerrar(self, horas)
        del self._estadias_ativas[registro.veiculo.placa]
        return registro

    def estadias_ativas(self) -> list[RegistroEstadia]:
        return list(self._estadias_ativas.values())
