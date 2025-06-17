import unittest
from datetime import datetime
from unittest.mock import Mock



class MockPaciente:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def __str__(self):
        return self.nombre

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


class Turno:
    def __init__(self, paciente=None, medico=None, fecha_hora=None, especialidad=None):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad
    
    def obtener_medico(self):
        return self.__medico
    
    def obtener_fecha_hora(self):
        return self.__fecha_hora
    
    def obtener_paciente(self):
        return self.__paciente
    
    def obtener_especialidad(self):
        return self.__especialidad
    
    def __str__(self):
        return f"Turno: {self.__paciente} con {self.__medico.obtener_matricula()} en {self.__especialidad} el {self.__fecha_hora}"

class TestTurno(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.paciente = MockPaciente("Juan Pérez")
        self.medico = MockMedico("Dr. García", "12345")
        self.fecha_hora = datetime(2024, 6, 15, 14, 30)
        self.especialidad = MockEspecialidad("Cardiología")
    
    def test_crear_turno_completo(self):
        """Test 1: Crear un turno con todos los parámetros"""
        turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        
        self.assertEqual(turno.obtener_paciente(), self.paciente)
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
        self.assertEqual(turno.obtener_especialidad(), self.especialidad)
    
    def test_crear_turno_vacio(self):
        """Test 2: Crear un turno sin parámetros (valores None)"""
        turno = Turno()
        
        self.assertIsNone(turno.obtener_paciente())
        self.assertIsNone(turno.obtener_medico())
        self.assertIsNone(turno.obtener_fecha_hora())
        self.assertIsNone(turno.obtener_especialidad())
    
    def test_obtener_medico(self):
        """Test 3: Verificar que obtener_medico() retorna el médico correcto"""
        turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        medico_obtenido = turno.obtener_medico()
        
        self.assertEqual(medico_obtenido, self.medico)
        self.assertEqual(medico_obtenido.obtener_matricula(), "12345")
    
    def test_obtener_fecha_hora(self):
        """Test 4: Verificar que obtener_fecha_hora() retorna la fecha correcta"""
        turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        fecha_obtenida = turno.obtener_fecha_hora()
        
        self.assertEqual(fecha_obtenida, self.fecha_hora)
        self.assertEqual(fecha_obtenida.year, 2024)
        self.assertEqual(fecha_obtenida.month, 6)
        self.assertEqual(fecha_obtenida.day, 15)
    
    def test_str_turno_completo(self):
        """Test 5: Verificar la representación string de un turno completo"""
        turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        expected_str = "Turno: Juan Pérez con 12345 en Cardiología el 2024-06-15 14:30:00"
        
        self.assertEqual(str(turno), expected_str)
    
    def test_crear_turno_solo_medico(self):
        """Test 6: Crear turno solo con médico"""
        turno = Turno(medico=self.medico)
        
        self.assertIsNone(turno.obtener_paciente())
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertIsNone(turno.obtener_fecha_hora())
        self.assertIsNone(turno.obtener_especialidad())
    
    def test_crear_turno_solo_fecha(self):
        """Test 7: Crear turno solo con fecha"""
        turno = Turno(fecha_hora=self.fecha_hora)
        
        self.assertIsNone(turno.obtener_paciente())
        self.assertIsNone(turno.obtener_medico())
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
        self.assertIsNone(turno.obtener_especialidad())
    
    def test_modificar_fecha_turno(self):
        """Test 8: Verificar que se puede crear turno con diferentes fechas"""
        nueva_fecha = datetime(2024, 12, 25, 10, 0)
        turno = Turno(self.paciente, self.medico, nueva_fecha, self.especialidad)
        
        self.assertEqual(turno.obtener_fecha_hora(), nueva_fecha)
        self.assertEqual(turno.obtener_fecha_hora().month, 12)
        self.assertEqual(turno.obtener_fecha_hora().day, 25)
    
    def test_multiples_turnos_mismo_medico(self):
        """Test 9: Crear múltiples turnos con el mismo médico"""
        paciente2 = MockPaciente("María López")
        fecha2 = datetime(2024, 6, 16, 9, 0)
        
        turno1 = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        turno2 = Turno(paciente2, self.medico, fecha2, self.especialidad)
        
        self.assertEqual(turno1.obtener_medico(), turno2.obtener_medico())
        self.assertNotEqual(turno1.obtener_paciente(), turno2.obtener_paciente())
        self.assertNotEqual(turno1.obtener_fecha_hora(), turno2.obtener_fecha_hora())
    
    def test_diferentes_especialidades(self):
        """Test 10: Crear turnos con diferentes especialidades"""
        especialidad_neuro = MockEspecialidad("Neurología")
        turno_cardio = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        turno_neuro = Turno(self.paciente, self.medico, self.fecha_hora, especialidad_neuro)
        
        self.assertEqual(str(turno_cardio.obtener_especialidad()), "Cardiología")
        self.assertEqual(str(turno_neuro.obtener_especialidad()), "Neurología")
        self.assertNotEqual(turno_cardio.obtener_especialidad(), turno_neuro.obtener_especialidad())

if __name__ == "__main__":
    unittest.main()