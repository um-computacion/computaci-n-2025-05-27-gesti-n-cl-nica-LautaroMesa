import unittest


class MockEspecialidad:
    def __init__(self, nombre, dias_atencion=None):
        self.nombre = nombre
        self.dias_atencion = dias_atencion or []
    
    def verificar_dia(self, dia):
        return dia.lower() in [d.lower() for d in self.dias_atencion]
    
    def obtener_especialidad(self):
        return self.nombre
    
    def __str__(self):
        dias_str = ", ".join(self.dias_atencion)
        return f"{self.nombre} - Días: {dias_str}"
    
    def __eq__(self, other):
        return isinstance(other, MockEspecialidad) and self.nombre == other.nombre


class Medico:
    def __init__(self, matricula: str, nombre: str, especialidad: str = None):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__especialidades = []

    def agregar_especialidad(self, especialidad):
        if not isinstance(especialidad, MockEspecialidad):  
            raise TypeError("Debe agregar una instancia de Especialidad")

        if especialidad in self.__especialidades:
            return  
        self.__especialidades.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula
    
    def obtener_nombre(self) -> str:
        return self.__nombre
    
    def obtener_especialidades(self) -> list:
        return self.__especialidades.copy()

    def obtener_especialidad_para_dia(self, dia: str):
        for esp in self.__especialidades:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self) -> str:
        if not self.__especialidades:
            return f"{self.__nombre} - Matrícula: {self.__matricula}\n  Sin especialidades asignadas"
        
        especialidades_str = "\n  ".join(str(esp) for esp in self.__especialidades)
        return f"{self.__nombre} - Matrícula: {self.__matricula}\n  {especialidades_str}"

class TestMedico(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.matricula = "MP-12345"
        self.nombre = "Dr. García"
        self.medico = Medico(self.matricula, self.nombre)
        
 
        self.cardiologia = MockEspecialidad("Cardiología", ["lunes", "miércoles", "viernes"])
        self.neurologia = MockEspecialidad("Neurología", ["martes", "jueves"])
        self.pediatria = MockEspecialidad("Pediatría", ["lunes", "martes", "miércoles"])
    
    def test_crear_medico_basico(self):
        """Test 1: Crear un médico con parámetros básicos"""
        medico = Medico("MP-54321", "Dra. López")
        
        self.assertEqual(medico.obtener_matricula(), "MP-54321")
        self.assertEqual(medico.obtener_nombre(), "Dra. López")
        self.assertEqual(len(medico.obtener_especialidades()), 0)
    
    def test_obtener_matricula(self):
        """Test 2: Verificar que obtener_matricula() retorna la matrícula correcta"""
        matricula_obtenida = self.medico.obtener_matricula()
        
        self.assertEqual(matricula_obtenida, self.matricula)
        self.assertIsInstance(matricula_obtenida, str)
    
    def test_agregar_especialidad_unica(self):
        """Test 3: Agregar una especialidad al médico"""
        self.medico.agregar_especialidad(self.cardiologia)
        
        especialidades = self.medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 1)
        self.assertIn(self.cardiologia, especialidades)
    
    def test_agregar_multiples_especialidades(self):
        """Test 4: Agregar múltiples especialidades diferentes"""
        self.medico.agregar_especialidad(self.cardiologia)
        self.medico.agregar_especialidad(self.neurologia)
        self.medico.agregar_especialidad(self.pediatria)
        
        especialidades = self.medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 3)
        self.assertIn(self.cardiologia, especialidades)
        self.assertIn(self.neurologia, especialidades)
        self.assertIn(self.pediatria, especialidades)
    
    def test_agregar_especialidad_duplicada(self):
        """Test 5: Intentar agregar la misma especialidad dos veces (no debe duplicarse)"""
        self.medico.agregar_especialidad(self.cardiologia)
        self.medico.agregar_especialidad(self.cardiologia)   
        
        especialidades = self.medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 1)
        self.assertEqual(especialidades[0], self.cardiologia)
    
    def test_agregar_tipo_incorrecto_error(self):
        """Test 6: Intentar agregar algo que no es una Especialidad debe lanzar TypeError"""
        with self.assertRaises(TypeError) as context:
            self.medico.agregar_especialidad("No es especialidad")
        
        self.assertIn("Debe agregar una instancia de Especialidad", str(context.exception))
        
        with self.assertRaises(TypeError):
            self.medico.agregar_especialidad(123)
        
        with self.assertRaises(TypeError):
            self.medico.agregar_especialidad(None)
    
    def test_obtener_especialidad_para_dia_existente(self):
        """Test 7: Obtener especialidad para un día específico que existe"""
        self.medico.agregar_especialidad(self.cardiologia)
        self.medico.agregar_especialidad(self.neurologia)
        
       
        especialidad_lunes = self.medico.obtener_especialidad_para_dia("lunes")
        self.assertEqual(especialidad_lunes, "Cardiología")
        
        especialidad_miercoles = self.medico.obtener_especialidad_para_dia("miércoles")
        self.assertEqual(especialidad_miercoles, "Cardiología")
        
        
        especialidad_martes = self.medico.obtener_especialidad_para_dia("martes")
        self.assertEqual(especialidad_martes, "Neurología")
    
    def test_obtener_especialidad_para_dia_inexistente(self):
        """Test 8: Intentar obtener especialidad para un día que no existe"""
        self.medico.agregar_especialidad(self.cardiologia)  
        
     
        especialidad_martes = self.medico.obtener_especialidad_para_dia("martes")
        self.assertIsNone(especialidad_martes)
        
        
        especialidad_domingo = self.medico.obtener_especialidad_para_dia("domingo")
        self.assertIsNone(especialidad_domingo)
    
    def test_str_medico_sin_especialidades(self):
        """Test 9: Verificar representación string de médico sin especialidades"""
        str_medico = str(self.medico)
        expected_str = "Dr. García - Matrícula: MP-12345\n  Sin especialidades asignadas"
        
        self.assertEqual(str_medico, expected_str)
        self.assertIn("Dr. García", str_medico)
        self.assertIn("MP-12345", str_medico)
        self.assertIn("Sin especialidades asignadas", str_medico)
    
    def test_str_medico_con_especialidades(self):
        """Test 10: Verificar representación string de médico con especialidades"""
        self.medico.agregar_especialidad(self.cardiologia)
        self.medico.agregar_especialidad(self.neurologia)
        
        str_medico = str(self.medico)
        
        
        self.assertIn("Dr. García", str_medico)
        self.assertIn("MP-12345", str_medico)
        
        
        self.assertIn("Cardiología", str_medico)
        self.assertIn("Neurología", str_medico)
        self.assertIn("lunes, miércoles, viernes", str_medico)
        self.assertIn("martes, jueves", str_medico)
        
       
        self.assertIn("\n  ", str_medico)

if __name__ == "__main__":
    unittest.main()