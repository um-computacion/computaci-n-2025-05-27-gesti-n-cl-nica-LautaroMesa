import unittest
from datetime import datetime


class MockPaciente:
    def __init__(self, dni, nombre, fecha_nacimiento):
        self.dni = dni
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
    
    def obtener_dni(self):
        return self.dni
    
    def __str__(self):
        return f"{self.nombre} - DNI: {self.dni} - Nacimiento: {self.fecha_nacimiento}"

class MockMedico:
    def __init__(self, nombre, matricula):
        self.nombre = nombre
        self.matricula = matricula
    
    def obtener_matricula(self):
        return self.matricula
    
    def __str__(self):
        return self.nombre

class MockEspecialidad:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def __str__(self):
        return self.nombre

class MockTurno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.especialidad = especialidad
    
    def obtener_medico(self):
        return self.medico
    
    def obtener_fecha_hora(self):
        return self.fecha_hora
    
    def __str__(self):
        return f"Turno: {self.paciente} con {self.medico.obtener_matricula()} en {self.especialidad} el {self.fecha_hora}"

class MockReceta:
    def __init__(self, paciente, medico, medicamentos, fecha=None):
        self.paciente = paciente
        self.medico = medico
        self.medicamentos = medicamentos
        self.fecha = fecha or datetime.now()
    
    def obtener_paciente(self):
        return self.paciente
    
    def obtener_medico(self):
        return self.medico
    
    def obtener_medicamentos(self):
        return self.medicamentos
    
    def __str__(self):
        meds = ", ".join(self.medicamentos)
        return f"Receta para {self.paciente} por {self.medico.obtener_matricula()} el {self.fecha.strftime('%d/%m/%Y')}:\n{meds}"


class HistoriaClinica:
    def __init__(self, paciente, turno=None, receta=None):
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
    
    def get_turnos(self):
        return self.__turnos.copy()
    
    def get_recetas(self):
        return self.__recetas.copy()

    def agregar_receta(self, receta):
        self.__recetas.append(receta)

    def agregar_turno(self, turno):
        self.__turnos.append(turno)

    def __str__(self):
        return f"HistoriaClinica(paciente={self.__paciente}, turno={self.__turno}, receta={self.__receta})"

class TestHistoriaClinica(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.paciente = MockPaciente("12345678", "Juan Pérez", "15/03/1985")
        self.medico = MockMedico("Dr. García", "MP-12345")
        self.especialidad = MockEspecialidad("Cardiología")
        self.fecha_turno = datetime(2024, 6, 17, 10, 30)
        self.turno = MockTurno(self.paciente, self.medico, self.fecha_turno, self.especialidad)
        self.receta = MockReceta(self.paciente, self.medico, ["Paracetamol 500mg", "Ibuprofeno 400mg"])
    
    def test_crear_historia_clinica_solo_paciente(self):
        """Test 1: Crear historia clínica solo con paciente"""
        historia = HistoriaClinica(self.paciente)
        
        self.assertEqual(historia.get_paciente(), self.paciente)
        self.assertIsNone(historia.get_turno())
        self.assertIsNone(historia.get_receta())
        self.assertEqual(len(historia.get_turnos()), 0)
        self.assertEqual(len(historia.get_recetas()), 0)
    
    def test_crear_historia_clinica_completa(self):
        """Test 2: Crear historia clínica con todos los parámetros"""
        historia = HistoriaClinica(self.paciente, self.turno, self.receta)
        
        self.assertEqual(historia.get_paciente(), self.paciente)
        self.assertEqual(historia.get_turno(), self.turno)
        self.assertEqual(historia.get_receta(), self.receta)
        self.assertEqual(len(historia.get_turnos()), 0)   
        self.assertEqual(len(historia.get_recetas()), 0)
    
    def test_get_paciente(self):
        """Test 3: Verificar que get_paciente() retorna el paciente correcto"""
        historia = HistoriaClinica(self.paciente)
        paciente_obtenido = historia.get_paciente()
        
        self.assertEqual(paciente_obtenido, self.paciente)
        self.assertEqual(paciente_obtenido.obtener_dni(), "12345678")
        self.assertIn("Juan Pérez", str(paciente_obtenido))
    
    def test_get_turno_y_receta_iniciales(self):
        """Test 4: Verificar getters de turno y receta iniciales"""
        historia = HistoriaClinica(self.paciente, self.turno, self.receta)
        
        turno_obtenido = historia.get_turno()
        receta_obtenida = historia.get_receta()
        
        self.assertEqual(turno_obtenido, self.turno)
        self.assertEqual(receta_obtenida, self.receta)
        self.assertEqual(turno_obtenido.obtener_medico(), self.medico)
        self.assertEqual(receta_obtenida.obtener_paciente(), self.paciente)
    
    def test_agregar_turno_unico(self):
        """Test 5: Agregar un turno a la lista de turnos"""
        historia = HistoriaClinica(self.paciente)
        historia.agregar_turno(self.turno)
        
        turnos = historia.get_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertIn(self.turno, turnos)
        self.assertEqual(turnos[0], self.turno)
    
    def test_agregar_multiples_turnos(self):
        """Test 6: Agregar múltiples turnos"""
        historia = HistoriaClinica(self.paciente)
        
     
        fecha2 = datetime(2024, 6, 20, 14, 0)
        fecha3 = datetime(2024, 6, 25, 16, 30)
        turno2 = MockTurno(self.paciente, self.medico, fecha2, self.especialidad)
        turno3 = MockTurno(self.paciente, self.medico, fecha3, self.especialidad)
        
        historia.agregar_turno(self.turno)
        historia.agregar_turno(turno2)
        historia.agregar_turno(turno3)
        
        turnos = historia.get_turnos()
        self.assertEqual(len(turnos), 3)
        self.assertIn(self.turno, turnos)
        self.assertIn(turno2, turnos)
        self.assertIn(turno3, turnos)
    
    def test_agregar_receta_unica(self):
        """Test 7: Agregar una receta a la lista de recetas"""
        historia = HistoriaClinica(self.paciente)
        historia.agregar_receta(self.receta)
        
        recetas = historia.get_recetas()
        self.assertEqual(len(recetas), 1)
        self.assertIn(self.receta, recetas)
        self.assertEqual(recetas[0], self.receta)
    
    def test_agregar_multiples_recetas(self):
        """Test 8: Agregar múltiples recetas"""
        historia = HistoriaClinica(self.paciente)
        
        
        receta2 = MockReceta(self.paciente, self.medico, ["Aspirina 100mg"])
        receta3 = MockReceta(self.paciente, self.medico, ["Omeprazol 20mg", "Vitamina D"])
        
        historia.agregar_receta(self.receta)
        historia.agregar_receta(receta2)
        historia.agregar_receta(receta3)
        
        recetas = historia.get_recetas()
        self.assertEqual(len(recetas), 3)
        self.assertIn(self.receta, recetas)
        self.assertIn(receta2, recetas)
        self.assertIn(receta3, recetas)
    
    def test_str_historia_clinica_completa(self):
        """Test 9: Verificar representación string con todos los parámetros"""
        historia = HistoriaClinica(self.paciente, self.turno, self.receta)
        str_historia = str(historia)
        
        self.assertIn("HistoriaClinica", str_historia)
        self.assertIn("paciente=", str_historia)
        self.assertIn("turno=", str_historia)
        self.assertIn("receta=", str_historia)
        
       
        self.assertIn("Juan Pérez", str_historia)
        self.assertIn("12345678", str_historia)
    
    def test_historia_clinica_completa_con_listas(self):
        """Test 10: Verificar funcionamiento completo con turnos y recetas adicionales"""
        historia = HistoriaClinica(self.paciente, self.turno, self.receta)
        
        turno_adicional = MockTurno(self.paciente, self.medico, datetime(2024, 7, 1, 9, 0), self.especialidad)
        receta_adicional = MockReceta(self.paciente, self.medico, ["Antibiótico"])
        
        historia.agregar_turno(turno_adicional)
        historia.agregar_receta(receta_adicional)
        
        self.assertEqual(historia.get_paciente(), self.paciente)
        self.assertEqual(historia.get_turno(), self.turno)
        self.assertEqual(historia.get_receta(), self.receta)
        
        turnos = historia.get_turnos()
        recetas = historia.get_recetas()
        
        self.assertEqual(len(turnos), 1)
        self.assertEqual(len(recetas), 1)
        self.assertIn(turno_adicional, turnos)
        self.assertIn(receta_adicional, recetas)
        
        turnos_obtenidos = historia.get_turnos()
        turnos_obtenidos.clear()  
        self.assertEqual(len(historia.get_turnos()), 1)  

if __name__ == "__main__":
    unittest.main()