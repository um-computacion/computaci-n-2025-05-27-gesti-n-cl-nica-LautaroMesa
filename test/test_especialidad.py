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


class TestEspecialidad(unittest.TestCase):
    
    def test_inicializacion_correcta(self):
        """Test 1: Verificar que la especialidad se inicializa correctamente"""
        especialidad = Especialidad("Cardiología", ["Lunes", "Miércoles", "Viernes"])
        self.assertEqual(especialidad.obtener_especialidad(), "Cardiología")
    
    def test_obtener_especialidad(self):
        """Test 2: Verificar que obtener_especialidad retorna el tipo correcto"""
        especialidad = Especialidad("Neurología", ["Martes", "Jueves"])
        self.assertEqual(especialidad.obtener_especialidad(), "Neurología")
    
    def test_verificar_dia_existente_minuscula(self):
        """Test 3: Verificar día existente en minúscula"""
        especialidad = Especialidad("Pediatría", ["Lunes", "Miércoles"])
        self.assertTrue(especialidad.verificar_dia("lunes"))
    
    def test_verificar_dia_existente_mayuscula(self):
        """Test 4: Verificar día existente en mayúscula"""
        especialidad = Especialidad("Dermatología", ["Martes", "Viernes"])
        self.assertTrue(especialidad.verificar_dia("MARTES"))
    
    def test_verificar_dia_existente_mixto(self):
        """Test 5: Verificar día existente con mayúsculas y minúsculas mezcladas"""
        especialidad = Especialidad("Oftalmología", ["Miércoles", "Sábado"])
        self.assertTrue(especialidad.verificar_dia("MiÉrCoLeS"))
    
    def test_verificar_dia_no_existente(self):
        """Test 6: Verificar día que no existe en la especialidad"""
        especialidad = Especialidad("Traumatología", ["Lunes", "Jueves"])
        self.assertFalse(especialidad.verificar_dia("Domingo"))
    
    def test_str_representation(self):
        """Test 7: Verificar la representación en string de la especialidad"""
        especialidad = Especialidad("Ginecología", ["Martes", "Jueves", "Sábado"])
        resultado_esperado = "Ginecología (Días: martes, jueves, sábado)"
        self.assertEqual(str(especialidad), resultado_esperado)
    
    def test_dias_se_convierten_a_minuscula(self):
        """Test 8: Verificar que los días se almacenan en minúscula internamente"""
        especialidad = Especialidad("Psiquiatría", ["LUNES", "MiÉrCoLeS", "viernes"])
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertTrue(especialidad.verificar_dia("miércoles"))
        self.assertTrue(especialidad.verificar_dia("viernes"))
    
    def test_especialidad_con_lista_vacia(self):
        """Test 9: Verificar especialidad con lista de días vacía"""
        especialidad = Especialidad("Medicina General", [])
        self.assertEqual(especialidad.obtener_especialidad(), "Medicina General")
        self.assertFalse(especialidad.verificar_dia("Lunes"))
        self.assertEqual(str(especialidad), "Medicina General (Días: )")
    
    def test_especialidad_con_un_solo_dia(self):
        """Test 10: Verificar especialidad con un solo día"""
        especialidad = Especialidad("Cirugía", ["Miércoles"])
        self.assertTrue(especialidad.verificar_dia("miércoles"))
        self.assertFalse(especialidad.verificar_dia("lunes"))
        self.assertEqual(str(especialidad), "Cirugía (Días: miércoles)")


if __name__ == "__main__":
    unittest.main()