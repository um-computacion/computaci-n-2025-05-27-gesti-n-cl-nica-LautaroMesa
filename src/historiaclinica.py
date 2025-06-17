
from src.paciente import Paciente
from src.turno import Turno
from src.receta import Receta
class HistoriaClinica:
    def __init__(self, paciente: Paciente, turno: Turno = None, receta: Receta = None):
        self.__paciente = paciente
        self.__turno = turno
        self.__receta = receta
        self.__turnos = []   
        self.__recetas = []  

    def get_paciente(self):
        return self.__paciente

    def get_turno(self):
        return self.__turno

    def get_receta(self):
        return self.__receta

    def agregar_receta(self, receta):
        self.__recetas.append(receta)

    def agregar_turno(self, turno):
        self.__turnos.append(turno)

    def __str__(self):
        return f"HistoriaClinica(paciente={self.__paciente}, turno={self.__turno}, receta={self.__receta})"
