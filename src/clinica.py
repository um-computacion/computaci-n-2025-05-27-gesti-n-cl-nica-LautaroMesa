from datetime import datetime
from src.paciente import Paciente
from src.exepciones import PacienteNoEncontradoException    
from src.exepciones import TurnoOcupadoException
from src.medico import Medico
from src.turno import Turno
from src.exepciones import MedicoNoDisponibleException
from src.receta import Receta
from src.exepciones import RecetaInvalidaException
from src.historiaclinica import HistoriaClinica
from src.exepciones import PacienteNoExisteError


class Clinica:
    def __init__(self):
        self.__pacientes: dict[str, Paciente] = {}
        self.__medicos: dict[str, Medico] = {}
        self.__turnos : list[Turno] = []
        self.__historias_clinicas : dict[str, HistoriaClinica ] = {}

    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        self.__medicos[medico.obtener_matricula()] = medico

    def obtener_pacientes(self):
        return list(self.__pacientes.values())

    def obtener_medicos(self):
        return list(self.__medicos.values())

    def obtener_medico_por_matricula(self, matricula):
        return self.__medicos.get(matricula)
    def obtener_medico_por_matricula(self, matricula):
        print(f"[DEBUG] Buscando médico con matrícula: '{matricula}'")
        print(f"[DEBUG] Claves registradas: {list(self.__medicos.keys())}")
        return self.__medicos.get(matricula)


    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        dia = self.obtener_dia_semana_en_espanol(fecha_hora)
        self.validar_especialidad_en_dia(medico, especialidad, dia)
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        self.__historias_clinicas[dni].agregar_turno(turno)

    def emitir_receta(self, dni, matricula, medicamentos):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        if not medicamentos:
            raise RecetaInvalidaException("Lista de medicamentos vacía.")
        receta = Receta(self.__pacientes[dni], self.__medicos[matricula], medicamentos)
        self.__historias_clinicas[dni].agregar_receta(receta)

    def obtener_turnos(self):
        return list(self.__turnos)

    def obtener_historia_clinica(self, dni: str):
        return self.__historias_clinicas.get(dni, None)

    def validar_existencia_paciente(self, dni:Paciente):
        if dni not in self.__pacientes:
            raise PacienteNoEncontradoException(f"No se encontró paciente con DNI {dni}")

    def validar_existencia_medico(self, matricula):
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException(f"No se encontró médico con matrícula {matricula}")

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        for turno in self.__turnos:
            if turno.obtener_medico().obtener_matricula() == matricula and turno.obtener_fecha_hora() == fecha_hora:
                raise TurnoOcupadoException("Turno ya ocupado.")

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]

    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada, dia):
        especialidad_real = medico.obtener_especialidad_para_dia(dia)
        if especialidad_real != especialidad_solicitada:
            raise MedicoNoDisponibleException("El médico no atiende esa especialidad ese día.")

