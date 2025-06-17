import unittest
class Especialidad:
    def __init__(self, tipo: str, dias: list[str]):
        self.__tipo = tipo
        self.__dias = [dia.lower() for dia in dias]

    def obtener_especialidad(self) -> str:
        return self.__tipo

    def verificar_dia(self, dia: str) -> bool:
        return dia.lower() in self.__dias

    def __str__(self) -> str:
        return f"{self.__tipo} (Días: {', '.join(self.__dias)})"
if __name__ == "__main__":
    unittest.main()