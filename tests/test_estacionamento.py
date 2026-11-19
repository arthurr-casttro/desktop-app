import pytest

from estacionamento.estadia import GeradorRecibo, RegistroEstadia
from estacionamento.vagas import Estacionamento, Vaga
from estacionamento.veiculos import Caminhonete, Carro, Moto, Veiculo
from main import MenuEstacionamento


def test_heranca():
    for classe in (Carro, Moto, Caminhonete):
        assert issubclass(classe, Veiculo)
    with pytest.raises(TypeError):
        Veiculo("abc1234")  # classe abstrata não pode ser instanciada


def test_polimorfismo_tarifa_carro_e_moto():
    carro = Carro("abc-1234")
    moto = Moto("xyz-9876")

    assert carro.calcular_tarifa(3) == 30.0
    assert moto.calcular_tarifa(3) == 15.0


def test_polimorfismo_lista_mista():
    veiculos: list[Veiculo] = [Carro("a1"), Moto("b2"), Caminhonete("c3")]
    est = Estacionamento("Central", 1)
    valores = [est.calcular_valor_saida(v, 2) for v in veiculos]
    assert valores == [20.0, 10.0, 35.0]  # caminhonete: 2*15 + 5 de taxa
    assert [v.tipo() for v in veiculos] == ["Carro", "Moto", "Caminhonete"]


def test_composicao_cria_vagas_e_bloqueia_quando_lotado():
    est = Estacionamento("Central", quantidade_vagas=2)
    v1 = est.buscar_vaga_livre()
    r1 = RegistroEstadia(Carro("aaa1111"), v1)

    v2 = est.buscar_vaga_livre()
    r2 = RegistroEstadia(Moto("bbb2222"), v2)

    assert len(est.vagas_livres()) == 0
    with pytest.raises(RuntimeError, match="lotado"):
        est.buscar_vaga_livre()

    r1.encerrar(est, horas=2)
    assert len(est.vagas_livres()) == 1
    assert r2.vaga.ocupada is True


def test_associacao_e_dependencia_gerador_recibo():
    est = Estacionamento("Central", quantidade_vagas=1)
    vaga = est.buscar_vaga_livre()
    carro = Carro("bra2e19")

    registro = RegistroEstadia(carro, vaga)
    assert registro.veiculo is carro
    assert registro.vaga is vaga

    valor = registro.encerrar(est, horas=4)
    assert valor == 40.0
    assert vaga.ocupada is False

    recibo = GeradorRecibo().gerar(registro)
    assert "BRA2E19" in recibo
    assert "Carro" in recibo
    assert "Horas: 4h" in recibo
    assert "R$ 40.00" in recibo


def test_validacoes_de_entrada_e_estado_invalido():
    carro = Carro("ccc3333")
    with pytest.raises(ValueError):
        carro.calcular_tarifa(0)
    with pytest.raises(ValueError):
        Carro("   ")
    with pytest.raises(ValueError):
        Estacionamento("Central", quantidade_vagas=0)

    est = Estacionamento("Central", quantidade_vagas=1)
    vaga = est.buscar_vaga_livre()
    registro = RegistroEstadia(carro, vaga)

    gerador = GeradorRecibo()
    with pytest.raises(RuntimeError):
        gerador.gerar(registro)

    registro.encerrar(est, horas=1)
    with pytest.raises(RuntimeError):
        registro.encerrar(est, horas=1)


def test_vaga_nao_libera_duas_vezes():
    vaga = Vaga("V01")
    with pytest.raises(RuntimeError, match="livre"):
        vaga.liberar()


def test_entrada_e_saida_pelo_estacionamento():
    est = Estacionamento("Central", 2)
    registro = est.registrar_entrada(Caminhonete("ddd4444"))
    assert registro.vaga.codigo == "V01"
    assert est.estadias_ativas() == [registro]

    with pytest.raises(RuntimeError, match="já está estacionado"):
        est.registrar_entrada(Carro("DDD4444"))

    saida = est.registrar_saida("ddd4444", 3)
    assert saida is registro
    assert saida.valor_pago == 50.0
    assert est.estadias_ativas() == []
    assert len(est.vagas_livres()) == 2

    with pytest.raises(RuntimeError, match="Nenhum veículo"):
        est.registrar_saida("ddd4444", 1)


def test_menu_fluxo_completo():
    respostas = iter(["1", "1", "abc1234", "4", "2", "abc1234", "2", "9", "0"])
    saidas: list[str] = []
    menu = MenuEstacionamento(
        Estacionamento("Teste", 2),
        entrada=lambda _: next(respostas),
        saida=saidas.append,
    )
    menu.executar()
    texto = "\n".join(saidas)
    assert "Carro (ABC1234) estacionado na vaga V01" in texto
    assert "V01: Carro (ABC1234)" in texto
    assert "Total: R$ 20.00" in texto
    assert "Opção inválida." in texto
    assert "Até logo!" in texto


def test_menu_mostra_erro_sem_encerrar():
    respostas = iter(["2", "zzz9999", "1", "0"])
    saidas: list[str] = []
    MenuEstacionamento(
        Estacionamento("Teste", 1),
        entrada=lambda _: next(respostas),
        saida=saidas.append,
    ).executar()
    assert any(s.startswith("Erro: Nenhum veículo") for s in saidas)
