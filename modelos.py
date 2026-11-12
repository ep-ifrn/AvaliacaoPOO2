from abc import ABC, abstractmethod
from dataclasses import dataclass

from excecoes import HorarioIndisponivelError, PacienteJaAgendadoError


@dataclass(frozen=True)
class Paciente:
    nome: str
    cartao_sus: str


class Atendimento(ABC):
    def __init__(self, paciente: Paciente) -> None:
        self._paciente: Paciente = paciente

    @property
    def paciente(self) -> Paciente:
        return self._paciente

    @abstractmethod
    def duracao_minutos(self) -> int:
        pass

    def __str__(self) -> str:
        return f"{type(self).__name__} - Paciente: {self._paciente.nome} ({self.duracao_minutos()} min)"


class Consulta(Atendimento):
    def __init__(self, paciente: Paciente, especialidade: str, retorno: bool = False) -> None:
        super().__init__(paciente)
        self.especialidade: str = especialidade
        self.retorno: bool = retorno

    def duracao_minutos(self) -> int:
        return 15 if self.retorno else 30


class Exame(Atendimento):
    def __init__(self, paciente: Paciente, tipo: str, jejum: bool = False) -> None:
        super().__init__(paciente)
        self.tipo: str = tipo
        self.jejum: bool = jejum

    def duracao_minutos(self) -> int:
        return 30 if self.jejum else 20


class Vacinacao(Atendimento):
    def __init__(self, paciente: Paciente, vacina: str, doses: int = 1) -> None:
        super().__init__(paciente)
        self.vacina: str = vacina
        self.doses: int = doses

    def duracao_minutos(self) -> int:
        return 10 * self.doses


class Agenda:
    def __init__(self, limite_minutos: int = 240) -> None:
        self.limite_minutos: int = limite_minutos
        self._atendimentos: list[Atendimento] = []

    @property
    def atendimentos(self) -> tuple[Atendimento, ...]:
        return tuple(self._atendimentos)

    @property
    def minutos_ocupados(self) -> int:
        return sum(atendimento.duracao_minutos() for atendimento in self._atendimentos)

    def agendar(self, atendimento: Atendimento) -> None:
        if any(agendado.paciente == atendimento.paciente for agendado in self._atendimentos):
            raise PacienteJaAgendadoError(
                f"O paciente {atendimento.paciente.nome} já possui atendimento agendado."
            )

        duracao_necessaria: int = atendimento.duracao_minutos()
        minutos_restantes: int = self.limite_minutos - self.minutos_ocupados
        if duracao_necessaria > minutos_restantes:
            raise HorarioIndisponivelError(
                f"Horário indisponível: são necessários {duracao_necessaria} min, mas restam {minutos_restantes} min."
            )

        self._atendimentos.append(atendimento)
