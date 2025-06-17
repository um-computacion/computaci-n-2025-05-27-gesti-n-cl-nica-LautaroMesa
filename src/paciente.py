import unittest
class Paciente:
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: str):
        self.__dni = dni
        self.__nombre = nombre
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni

    def __str__(self) -> str:
        return f"{self.__nombre} - DNI: {self.__dni} - Nacimiento: {self.__fecha_nacimiento}"
if __name__ == "__main__":
    unittest.main()