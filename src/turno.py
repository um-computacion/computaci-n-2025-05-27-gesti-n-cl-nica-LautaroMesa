from src.paciente import Paciente
from datetime import datetime
from src.medico import Medico
from src.especialidad import Especialidad
import unittest
class Turno:
    def __init__(self, paciente: str = Paciente, medico: str= Medico, fecha_hora: str = datetime, especialidad: str = Especialidad):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad

    def obtener_medico(self):
        return self.__medico

    def obtener_fecha_hora(self):
        return self.__fecha_hora

    def __str__(self):
        return f"Turno: {self.__paciente} con {self.__medico.obtener_matricula()} en {self.__especialidad} el {self.__fecha_hora}"
if __name__ == "__main__":
    unittest.main() 