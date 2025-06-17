import unittest
class Paciente:
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: str):
        self.__dni = dni
        self.__nombre = nombre
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni
    
    def obtener_nombre(self) -> str:
        return self.__nombre
    
    def obtener_fecha_nacimiento(self) -> str:
        return self.__fecha_nacimiento

    def __str__(self) -> str:
        return f"{self.__nombre} - DNI: {self.__dni} - Nacimiento: {self.__fecha_nacimiento}"

class TestPaciente(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.dni_valido = "12345678"
        self.nombre_valido = "Juan Pérez"
        self.fecha_nacimiento_valida = "15/03/1985"
    
    def test_crear_paciente_completo(self):
        """Test 1: Crear un paciente con todos los parámetros válidos"""
        paciente = Paciente(self.dni_valido, self.nombre_valido, self.fecha_nacimiento_valida)
        
        self.assertEqual(paciente.obtener_dni(), self.dni_valido)
        self.assertEqual(paciente.obtener_nombre(), self.nombre_valido)
        self.assertEqual(paciente.obtener_fecha_nacimiento(), self.fecha_nacimiento_valida)
    
    def test_obtener_dni(self):
        """Test 2: Verificar que obtener_dni() retorna el DNI correcto"""
        dni_test = "87654321"
        paciente = Paciente(dni_test, "María López", "22/07/1992")
        
        dni_obtenido = paciente.obtener_dni()
        self.assertEqual(dni_obtenido, dni_test)
        self.assertIsInstance(dni_obtenido, str)
    
    def test_obtener_nombre(self):
        """Test 3: Verificar que obtener_nombre() retorna el nombre correcto"""
        nombre_test = "Carlos Rodríguez"
        paciente = Paciente("11223344", nombre_test, "10/12/1978")
        
        nombre_obtenido = paciente.obtener_nombre()
        self.assertEqual(nombre_obtenido, nombre_test)
        self.assertIsInstance(nombre_obtenido, str)
    
    def test_obtener_fecha_nacimiento(self):
        """Test 4: Verificar que obtener_fecha_nacimiento() retorna la fecha correcta"""
        fecha_test = "05/09/1990"
        paciente = Paciente("55667788", "Ana García", fecha_test)
        
        fecha_obtenida = paciente.obtener_fecha_nacimiento()
        self.assertEqual(fecha_obtenida, fecha_test)
        self.assertIsInstance(fecha_obtenida, str)
    
    def test_str_representacion_completa(self):
        """Test 5: Verificar la representación string del paciente"""
        paciente = Paciente(self.dni_valido, self.nombre_valido, self.fecha_nacimiento_valida)
        expected_str = "Juan Pérez - DNI: 12345678 - Nacimiento: 15/03/1985"
        
        self.assertEqual(str(paciente), expected_str)
    
    def test_paciente_nombre_compuesto(self):
        """Test 6: Crear paciente con nombre y apellidos compuestos"""
        nombre_compuesto = "María José Fernández García"
        paciente = Paciente("99887766", nombre_compuesto, "28/02/1988")
        
        self.assertEqual(paciente.obtener_nombre(), nombre_compuesto)
        str_paciente = str(paciente)
        self.assertIn(nombre_compuesto, str_paciente)
        self.assertIn("99887766", str_paciente)
    
    def test_dni_diferentes_formatos(self):
        """Test 7: Probar con diferentes formatos de DNI"""
        
        paciente1 = Paciente("12345678", "Persona Uno", "01/01/2000")
        self.assertEqual(paciente1.obtener_dni(), "12345678")
        
        
        paciente2 = Paciente("1234567", "Persona Dos", "02/02/2000")
        self.assertEqual(paciente2.obtener_dni(), "1234567")
        
        
        paciente3 = Paciente("12345678A", "Persona Tres", "03/03/2000")
        self.assertEqual(paciente3.obtener_dni(), "12345678A")
    
    def test_fechas_diferentes_formatos(self):
        """Test 8: Probar con diferentes formatos de fecha de nacimiento"""
        
        paciente1 = Paciente("11111111", "Paciente Uno", "15/06/1995")
        self.assertEqual(paciente1.obtener_fecha_nacimiento(), "15/06/1995")
        
        
        paciente2 = Paciente("22222222", "Paciente Dos", "20-12-1987")
        self.assertEqual(paciente2.obtener_fecha_nacimiento(), "20-12-1987")
        
        
        paciente3 = Paciente("33333333", "Paciente Tres", "1990/03/25")
        self.assertEqual(paciente3.obtener_fecha_nacimiento(), "1990/03/25")
    
    def test_str_con_caracteres_especiales(self):
        """Test 9: Verificar string con nombres que contienen caracteres especiales"""
        nombre_con_acentos = "José María Ñoño"
        paciente = Paciente("44556677", nombre_con_acentos, "12/05/1975")
        
        str_paciente = str(paciente)
        expected_str = "José María Ñoño - DNI: 44556677 - Nacimiento: 12/05/1975"
        
        self.assertEqual(str_paciente, expected_str)
        self.assertIn("José María Ñoño", str_paciente)
        self.assertIn("ñ", str_paciente.lower())
    
    def test_comparar_pacientes_diferentes(self):
        """Test 10: Verificar que pacientes diferentes son distintos objetos"""
        paciente1 = Paciente("11111111", "Juan Pérez", "01/01/1980")
        paciente2 = Paciente("22222222", "María García", "02/02/1990")
        paciente3 = Paciente("11111111", "Juan Pérez", "01/01/1980")  
        
        self.assertNotEqual(paciente1, paciente3)  
        
        self.assertEqual(paciente1.obtener_dni(), paciente3.obtener_dni())
        self.assertEqual(paciente1.obtener_nombre(), paciente3.obtener_nombre())
        self.assertEqual(paciente1.obtener_fecha_nacimiento(), paciente3.obtener_fecha_nacimiento())
        
        
        self.assertNotEqual(paciente1.obtener_dni(), paciente2.obtener_dni())
        self.assertNotEqual(paciente1.obtener_nombre(), paciente2.obtener_nombre())
        self.assertNotEqual(paciente1.obtener_fecha_nacimiento(), paciente2.obtener_fecha_nacimiento())

if __name__ == "__main__":
    unittest.main()