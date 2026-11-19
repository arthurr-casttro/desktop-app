# Estacionamento — POO em Python

Aplicação desktop de terminal (não web) para controlar entrada e saída de veículos
de um estacionamento, com cálculo de tarifa por tipo de veículo e emissão de recibo.

## Como rodar

```powershell
.\.venv\Scripts\python.exe main.py          # menu interativo
.\.venv\Scripts\python.exe -m pytest -q     # testes
```

Requer Python 3.10+ (sem dependências externas além do `pytest` para os testes).

## Estrutura

```
estacionamento/
  veiculos.py   Veiculo (abstrata), Carro, Moto, Caminhonete
  vagas.py      Vaga, Estacionamento
  estadia.py    RegistroEstadia, GeradorRecibo
main.py         MenuEstacionamento (interface de terminal)
docs/uml.mmd    Diagrama de classes (Mermaid)
tests/          Testes com pytest
```

## Conceitos de POO

| Conceito | Onde aparece |
|---|---|
| **Herança** | `Carro`, `Moto` e `Caminhonete` herdam da classe abstrata `Veiculo` |
| **Abstração / encapsulamento** | `Veiculo` (ABC com métodos abstratos); `_placa`, `_ocupada`, `_vagas` expostos só via `@property`/métodos |
| **Polimorfismo** | `Estacionamento.calcular_valor_saida()` chama `veiculo.calcular_tarifa()` sem saber a classe concreta; `Caminhonete` sobrescreve `calcular_tarifa` usando `super()` |
| **Composição** | `Estacionamento` cria e possui suas `Vaga`s |
| **Agregação** | `Estacionamento` guarda os `RegistroEstadia` ativos |
| **Associação** | `RegistroEstadia` liga um `Veiculo` a uma `Vaga`; `MenuEstacionamento` mantém um `Estacionamento` |
| **Dependência** | `RegistroEstadia.encerrar()` usa um `Estacionamento` recebido por parâmetro; `GeradorRecibo.gerar()` usa um `RegistroEstadia`; `MenuEstacionamento` usa `GeradorRecibo` só ao emitir o recibo |

## Tarifas

| Veículo | Regra |
|---|---|
| Carro | R$ 10,00/hora |
| Moto | R$ 5,00/hora |
| Caminhonete | R$ 15,00/hora + R$ 5,00 de taxa fixa |
