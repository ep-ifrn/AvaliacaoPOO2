from excecoes import AgendaError
from modelos import Agenda, Atendimento, Consulta, Exame, Paciente, Vacinacao

def exibir_resumo(agenda: Agenda) -> None:
    print(f"Minutos ocupados: {agenda.minutos_ocupados}/{agenda.limite_minutos}")
    for atendimento in agenda.atendimentos:
        print(f"{atendimento}")

def main() -> None:
    agenda: Agenda = Agenda(limite_minutos=100)

    ana: Paciente = Paciente("Ana Souza", "700000000000001")
    leo: Paciente = Paciente("Leo Lima", "700000000000002")
    rui:Paciente = Paciente("Rui Alves", "700000000000003")
    bia: Paciente = Paciente("Bia Costa", "700000000000004")

    tentativas: list[Atendimento] = [
        Consulta(ana, "Clínica Geral"),
        Consulta(leo, "Pediatria", retorno=True),
        Exame(rui, "Glicemia", jejum=True),
        Vacinacao(ana, "Influenza"),
        Vacinacao(bia, "Hepatite B", doses=3),
        Vacinacao(bia, "Hepatite B", doses=2),
    ]

    for item in tentativas:
        try:
            agenda.agendar(item)
            print(f"[AGENDADO] {item}")
        except AgendaError as erro:
            print(f"[ERRO] {erro}")

    print()
    print("--- Resumo da agenda ---")
    exibir_resumo(agenda)


if __name__ == "__main__":
    main()