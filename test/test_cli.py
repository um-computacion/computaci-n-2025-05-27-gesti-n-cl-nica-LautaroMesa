import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
from datetime import datetime

class Paciente:
    def __init__(self, dni, nombre, fecha_nacimiento):
        self.dni = dni
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
    
    def obtener_dni(self):
        return self.dni
    
    def __str__(self):
        return f"Paciente: {self.nombre} (DNI: {self.dni})"

class Medico:
    def __init__(self, matricula, nombre, especialidad):
        self.matricula = matricula
        self.nombre = nombre
        self.especialidad = especialidad
        self.especialidades = []
    
    def obtener_matricula(self):
        return self.matricula
    
    def agregar_especialidad(self, especialidad):
        self.especialidades.append(especialidad)
    
    def __str__(self):
        return f"Médico: {self.nombre} (Matrícula: {self.matricula})"

class Especialidad:
    def __init__(self, tipo, dias):
        self.tipo = tipo
        self.dias = dias

class Turno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.especialidad = especialidad
    
    def __str__(self):
        return f"Turno: {self.paciente.nombre} con {self.medico.nombre} - {self.fecha_hora}"

class HistoriaClinica:
    def __init__(self, paciente):
        self.paciente = paciente
    
    def __str__(self):
        return f"Historia clínica de {self.paciente.nombre}"

class Receta:
    def __init__(self, paciente, medico, medicamentos):
        self.paciente = paciente
        self.medico = medico
        self.medicamentos = medicamentos
    
    def __str__(self):
        return f"Receta para {self.paciente.nombre}: {', '.join(self.medicamentos)}"

class PacienteNoExisteError(Exception):
    pass

class MedicoYaExisteError(Exception):
    pass

class MedicoNoExisteError(Exception):
    pass

class EspecialidadNoDisponibleError(Exception):
    pass

class TurnoDuplicadoError(Exception):
    pass

class RecetaInvalidaError(Exception):
    pass

class FechaIncorrectaError(Exception):
    pass

class Clinica:
    def __init__(self):
        self.pacientes = []
        self.medicos = []
        self.turnos = []
    
    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)
    
    def agregar_medico(self, medico):
        self.medicos.append(medico)
    
    def obtener_medico_por_matricula(self, matricula):
        for medico in self.medicos:
            if medico.obtener_matricula() == matricula:
                return medico
        return None
    
    def agendar_turno(self, dni, matricula, especialidad, fecha):
        turno = Turno(Mock(), Mock(), fecha, especialidad)
        self.turnos.append(turno)
    
    def emitir_receta(self, dni, matricula, medicamentos):
        return Receta(Mock(), Mock(), medicamentos)
    
    def obtener_historia_clinica(self, dni):
        return HistoriaClinica(Mock())
    
    def obtener_turnos(self):
        return self.turnos
    
    def obtener_pacientes(self):
        return self.pacientes
    
    def obtener_medicos(self):
        return self.medicos

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        print("\n--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")

    def agregar_paciente(self):
        try:
            dni = input("DNI: ").strip()
            if not dni:
                print("Error: DNI no puede estar vacío.")
                return
            nombre = input("Nombre Completo: ").strip()
            if not nombre:
                print("Error: Nombre no puede estar vacío.")
                return
            fecha = input("Fecha nacimiento (DD/MM/AAAA): ").strip()
            if not fecha:
                print("Error: Fecha de nacimiento no puede estar vacía.")
                return
            paciente = Paciente(dni, nombre, fecha)
            self.clinica.agregar_paciente(paciente)
            print("Paciente agregado exitosamente.")
        except (PacienteNoExisteError, FechaIncorrectaError) as e:
            print(f"Error: {e}")

    def agregar_medico(self):
        try:
            matricula = input("Matrícula: ").strip()
            if not matricula:
                print("Error: Matrícula no puede estar vacía.")
                return
            nombre = input("Nombre: ").strip()
            if not nombre:
                print("Error: Nombre no puede estar vacío.")
                return
            especialidad = input("Especialidad: ").strip()
            if not especialidad:    
                print("Error: Especialidad no puede estar vacía.")
                return
            medico = Medico(matricula, nombre, especialidad)
            self.clinica.agregar_medico(medico)
            print("Médico agregado exitosamente.")
        except MedicoYaExisteError as e:
            print(f"Error: {e}")

    def agregar_especialidad(self):
        try:
            matricula = input("Matrícula del médico: ").strip()
            tipo = input("Especialidad: ").strip()
            dias = []
            print("Ingrese días (escriba 'fin' para terminar):")
            while True:
                dia = input("Día: ").strip().lower()
                if dia == "fin": break
                if dia: dias.append(dia)
            especialidad = Especialidad(tipo, dias)
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            if medico:
                medico.agregar_especialidad(especialidad)
                print("Especialidad agregada")
            else:
                raise MedicoNoExisteError("Médico no encontrado")
        except (ValueError, MedicoNoExisteError) as e:
            print(f"Error: {e}")

    def agendar_turno(self):
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matrícula del médico: ").strip()
            especialidad = input("Especialidad: ").strip()
            fecha_str = input("Fecha y hora (DD/MM/AAAA HH:MM): ").strip()
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha)
            print("Turno agendado")
        except (PacienteNoExisteError, MedicoNoExisteError, EspecialidadNoDisponibleError, 
                TurnoDuplicadoError, ValueError) as e:
            print(f"Error: {e}")

    def emitir_receta(self):
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Médico que receta (matrícula): ").strip()
            meds_str = input("Medicamentos (separados por coma): ").strip()
            medicamentos = [m.strip() for m in meds_str.split(",") if m.strip()]
            receta = self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("Receta emitida")
            print(receta)
        except (PacienteNoExisteError, MedicoNoExisteError, RecetaInvalidaError, ValueError) as e:
            print(f"Error: {e}")

    def ver_historia(self):
        try:
            dni = input("DNI del paciente: ").strip()
            historia = self.clinica.obtener_historia_clinica(dni)
            print(historia)
        except PacienteNoExisteError as e:
            print(f"Error: {e}")

    def ver_turnos(self):
        for t in self.clinica.obtener_turnos():
            print(t)

    def ver_pacientes(self):
        for p in self.clinica.obtener_pacientes():
            print(p)

    def ver_medicos(self):
        for m in self.clinica.obtener_medicos():
            print(m)


class TestCLI(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.cli = CLI()
    
    @patch('builtins.input', side_effect=['12345678', 'Juan Pérez', '01/01/1990'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agregar_paciente_exitoso(self, mock_stdout, mock_input):
        """Test 1: Agregar paciente exitosamente"""
        self.cli.agregar_paciente()
        output = mock_stdout.getvalue()
        self.assertIn("Paciente agregado exitosamente", output)
        self.assertEqual(len(self.cli.clinica.obtener_pacientes()), 1)
    
    @patch('builtins.input', side_effect=['', 'Juan Pérez', '01/01/1990'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agregar_paciente_dni_vacio(self, mock_stdout, mock_input):
        """Test 2: Error al agregar paciente con DNI vacío"""
        self.cli.agregar_paciente()
        output = mock_stdout.getvalue()
        self.assertIn("Error: DNI no puede estar vacío", output)
        self.assertEqual(len(self.cli.clinica.obtener_pacientes()), 0)
    
    @patch('builtins.input', side_effect=['MED001', 'Dr. García', 'Cardiología'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agregar_medico_exitoso(self, mock_stdout, mock_input):
        """Test 3: Agregar médico exitosamente"""
        self.cli.agregar_medico()
        output = mock_stdout.getvalue()
        self.assertIn("Médico agregado exitosamente", output)
        self.assertEqual(len(self.cli.clinica.obtener_medicos()), 1)
    
    @patch('builtins.input', side_effect=['', 'Dr. García', 'Cardiología'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agregar_medico_matricula_vacia(self, mock_stdout, mock_input):
        """Test 4: Error al agregar médico con matrícula vacía"""
        self.cli.agregar_medico()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Matrícula no puede estar vacía", output)
        self.assertEqual(len(self.cli.clinica.obtener_medicos()), 0)
    
    @patch('builtins.input', side_effect=['MED001', 'Cardiología', 'lunes', 'miércoles', 'fin'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agregar_especialidad_exitoso(self, mock_stdout, mock_input):
        """Test 5: Agregar especialidad a médico exitosamente"""
        medico = Medico('MED001', 'Dr. García', 'Cardiología')
        self.cli.clinica.agregar_medico(medico)
        
        self.cli.agregar_especialidad()
        output = mock_stdout.getvalue()
        self.assertIn("Especialidad agregada", output)
    
    @patch('builtins.input', side_effect=['MED999', 'Cardiología', 'lunes', 'fin'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agregar_especialidad_medico_no_existe(self, mock_stdout, mock_input):
        """Test 6: Error al agregar especialidad a médico inexistente"""
        self.cli.agregar_especialidad()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Médico no encontrado", output)
    
    @patch('builtins.input', side_effect=['12345678', 'MED001', 'Cardiología', '17/06/2024 10:00'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agendar_turno_exitoso(self, mock_stdout, mock_input):
        """Test 7: Agendar turno exitosamente"""
        self.cli.agendar_turno()
        output = mock_stdout.getvalue()
        self.assertIn("Turno agendado", output)
        self.assertEqual(len(self.cli.clinica.obtener_turnos()), 1)
    
    @patch('builtins.input', side_effect=['12345678', 'MED001', 'Cardiología', 'fecha_invalida'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_agendar_turno_fecha_invalida(self, mock_stdout, mock_input):
        """Test 8: Error al agendar turno con fecha inválida"""
        self.cli.agendar_turno()
        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
    
    @patch('builtins.input', side_effect=['12345678', 'MED001', 'Aspirina, Paracetamol'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_emitir_receta_exitoso(self, mock_stdout, mock_input):
        """Test 9: Emitir receta exitosamente"""
        self.cli.emitir_receta()
        output = mock_stdout.getvalue()
        self.assertIn("Receta emitida", output)
    
    @patch('builtins.input', side_effect=['12345678'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_ver_historia_clinica(self, mock_stdout, mock_input):
        """Test 10: Ver historia clínica"""
        self.cli.ver_historia()
        output = mock_stdout.getvalue()
        self.assertIn("Historia clínica", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_menu(self, mock_stdout):
        """Test bonus: Verificar que se muestra el menú correctamente"""
        self.cli.mostrar_menu()
        output = mock_stdout.getvalue()
        self.assertIn("--- Menú Clínica ---", output)
        self.assertIn("1) Agregar paciente", output)
        self.assertIn("0) Salir", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_ver_pacientes_vacio(self, mock_stdout):
        """Test adicional: Ver lista de pacientes vacía"""
        self.cli.ver_pacientes()
        # No debería imprimir nada si no hay pacientes
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), "")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_ver_medicos_con_datos(self, mock_stdout):
        """Test adicional: Ver lista de médicos con datos"""
        medico = Medico('MED001', 'Dr. García', 'Cardiología')
        self.cli.clinica.agregar_medico(medico)
        
        self.cli.ver_medicos()
        output = mock_stdout.getvalue()
        self.assertIn("Dr. García", output)
        self.assertIn("MED001", output)


if __name__ == "__main__":
    unittest.main()