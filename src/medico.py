from src.especialidad import Especialidad
class Medico:
    def __init__(self, matricula: str, nombre: str, especialidad: str):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__especialidades : list[Especialidad] = [] 

    def agregar_especialidad(self, especialidad: Especialidad):
        if not isinstance(especialidad, Especialidad):
            raise TypeError("Debe agregar una instancia de Especialidad")

        if especialidad in self.__especialidades:
            return  
        self.__especialidades.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula

    def obtener_especialidad_para_dia(self, dia: str):
        for esp in self.__especialidades:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades_str = "\n  ".join(str(esp) for esp in self.__especialidades)
        return f"{self.__nombre} - Matrícula: {self.__matricula}\n  {especialidades_str}"
