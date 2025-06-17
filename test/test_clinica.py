import unittest
from datetime import datetime
from unittest.mock import Mock, MagicMock


class Paciente:
    def __init__(self, dni, nombre):
        self.dni = dni
        self.nombre = nombre
    
    def obtener_dni(self):
        return self.dni

class Medico:
    def __init__(self, matricula, nombre):
        self.matricula = matricula
        self.nombre = nombre
        self.especialidades = {}
    
    def obtener_matricula(self):
        return self.matricula
    
    def obtener_especialidad_para_dia(self, dia):
        return self.especialidades.get(dia)
    
    def agregar_especialidad_dia(self, dia, especialidad):
        self.especialidades[dia] = especialidad

class Turno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.especialidad = especialidad
    
    def obtener_medico(self):
        return self.medico
    
    def obtener_fecha_hora(self):
        return self.fecha_hora

class Receta:
    def __init__(self, paciente, medico, medicamentos):
        self.paciente = paciente
        self.medico = medico
        self.medicamentos = medicamentos

class HistoriaClinica:
    def __init__(self, paciente):
        self.paciente = paciente
        self.turnos = []
        self.recetas = []
    
    def agregar_turno(self, turno):
        self.turnos.append(turno)
    
    def agregar_receta(self, receta):
        self.recetas.append(receta)

# Excepciones simuladas
class PacienteNoEncontradoException(Exception):
    pass

class TurnoOcupadoException(Exception):
    pass

class MedicoNoDisponibleException(Exception):
    pass

class RecetaInvalidaException(Exception):
    pass

class PacienteNoExisteError(Exception):
    pass


class Clinica:
    def __init__(self):
        self.__pacientes: dict[str, Paciente] = {}
        self.__medicos: dict[str, Medico] = {}
        self.__turnos : list[Turno] = []
        self.__historias_clinicas : dict[str, HistoriaClinica ] = {}

    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        self.__medicos[medico.obtener_matricula()] = medico

    def obtener_pacientes(self):
        return list(self.__pacientes.values())

    def obtener_medicos(self):
        return list(self.__medicos.values())

    def obtener_medico_por_matricula(self, matricula):
        return self.__medicos.get(matricula)

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        dia = self.obtener_dia_semana_en_espanol(fecha_hora)
        self.validar_especialidad_en_dia(medico, especialidad, dia)
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        self.__historias_clinicas[dni].agregar_turno(turno)

    def emitir_receta(self, dni, matricula, medicamentos):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        if not medicamentos:
            raise RecetaInvalidaException("Lista de medicamentos vacía.")
        receta = Receta(self.__pacientes[dni], self.__medicos[matricula], medicamentos)
        self.__historias_clinicas[dni].agregar_receta(receta)

    def obtener_turnos(self):
        return list(self.__turnos)

    def obtener_historia_clinica(self, dni: str):
        return self.__historias_clinicas.get(dni, None)

    def validar_existencia_paciente(self, dni):
        if dni not in self.__pacientes:
            raise PacienteNoEncontradoException(f"No se encontró paciente con DNI {dni}")

    def validar_existencia_medico(self, matricula):
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException(f"No se encontró médico con matrícula {matricula}")

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        for turno in self.__turnos:
            if turno.obtener_medico().obtener_matricula() == matricula and turno.obtener_fecha_hora() == fecha_hora:
                raise TurnoOcupadoException("Turno ya ocupado.")

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]

    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada, dia):
        especialidad_real = medico.obtener_especialidad_para_dia(dia)
        if especialidad_real != especialidad_solicitada:
            raise MedicoNoDisponibleException("El médico no atiende esa especialidad ese día.")


class TestClinica(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.clinica = Clinica()
        self.paciente = Paciente("12345678", "Juan Pérez")
        self.medico = Medico("MED001", "Dr. García")
        self.medico.agregar_especialidad_dia("lunes", "Cardiología")
        
    def test_agregar_paciente(self):
        """Test 1: Verificar que se puede agregar un paciente correctamente"""
        self.clinica.agregar_paciente(self.paciente)
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "12345678")
        
    def test_agregar_medico(self):
        """Test 2: Verificar que se puede agregar un médico correctamente"""
        self.clinica.agregar_medico(self.medico)
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "MED001")
        
    def test_obtener_medico_por_matricula_existente(self):
        """Test 3: Verificar obtención de médico por matrícula existente"""
        self.clinica.agregar_medico(self.medico)
        medico_encontrado = self.clinica.obtener_medico_por_matricula("MED001")
        self.assertIsNotNone(medico_encontrado)
        self.assertEqual(medico_encontrado.obtener_matricula(), "MED001")
        
    def test_obtener_medico_por_matricula_inexistente(self):
        """Test 4: Verificar obtención de médico por matrícula inexistente"""
        medico_encontrado = self.clinica.obtener_medico_por_matricula("MED999")
        self.assertIsNone(medico_encontrado)
        
    def test_agendar_turno_exitoso(self):
        """Test 5: Verificar agendamiento exitoso de turno"""
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha_hora = datetime(2024, 6, 17, 10, 0)  
        
        self.clinica.agendar_turno("12345678", "MED001", "Cardiología", fecha_hora)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        
    def test_agendar_turno_paciente_no_encontrado(self):
        """Test 6: Verificar excepción al agendar turno con paciente inexistente"""
        self.clinica.agregar_medico(self.medico)
        fecha_hora = datetime(2024, 6, 17, 10, 0)
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "MED001", "Cardiología", fecha_hora)
            
    def test_agendar_turno_medico_no_encontrado(self):
        """Test 7: Verificar excepción al agendar turno con médico inexistente"""
        self.clinica.agregar_paciente(self.paciente)
        fecha_hora = datetime(2024, 6, 17, 10, 0)
        
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "MED999", "Cardiología", fecha_hora)
            
    def test_turno_duplicado(self):
        """Test 8: Verificar excepción al intentar agendar turno duplicado"""
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha_hora = datetime(2024, 6, 17, 10, 0)  
        
        
        self.clinica.agendar_turno("12345678", "MED001", "Cardiología", fecha_hora)
        
        
        paciente2 = Paciente("87654321", "María López")
        self.clinica.agregar_paciente(paciente2)
        
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "MED001", "Cardiología", fecha_hora)
            
    def test_emitir_receta_exitosa(self):
        """Test 9: Verificar emisión exitosa de receta"""
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        medicamentos = ["Aspirina", "Paracetamol"]
        
        self.clinica.emitir_receta("12345678", "MED001", medicamentos)
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.recetas), 1)
        
    def test_emitir_receta_medicamentos_vacios(self):
        """Test 10: Verificar excepción al emitir receta con medicamentos vacíos"""
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "MED001", [])
            
    def test_obtener_dia_semana_en_espanol(self):
        """Test bonus: Verificar conversión correcta de día de la semana"""
        
        fecha_lunes = datetime(2024, 6, 17)
        dia = self.clinica.obtener_dia_semana_en_espanol(fecha_lunes) 
        self.assertEqual(dia, "lunes")
        
        
        fecha_viernes = datetime(2024, 6, 21)
        dia = self.clinica.obtener_dia_semana_en_espanol(fecha_viernes)
        self.assertEqual(dia, "viernes")


if __name__ == "__main__":
    unittest.main()