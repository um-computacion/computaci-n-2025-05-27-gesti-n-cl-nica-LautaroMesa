
from datetime import datetime
from src.paciente import Paciente
from src.medico import Medico
class Receta:
    def __init__(self, paciente: Paciente, medico : Medico, medicamentos: list[str], fecha: datetime = None):
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos
        self.__fecha = datetime.now()

    def __str__(self):  
        meds = ", ".join(self.__medicamentos)
        return f"Receta para {self.__paciente} por {self.__medico.obtener_matricula()} el {self.__fecha.strftime('%d/%m/%Y')}:\n{meds}"

