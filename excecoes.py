class AgendaError(Exception):
    pass

class HorarioIndisponivelError(AgendaError):
    pass

class PacienteJaAgendadoError(AgendaError):
    pass

    