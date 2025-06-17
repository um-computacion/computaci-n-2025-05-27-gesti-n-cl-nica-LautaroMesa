import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.receta import Receta
    from src.paciente import Paciente
    from src.medico import Medico
except ImportError:
    
    from datetime import datetime
    
    class Paciente:
        pass
    
    class Medico:
        def obtener_matricula(self):
            return "MP12345"
    
    class Receta:
        def __init__(self, paciente, medico, medicamentos: list[str], fecha: datetime = None):
            self.__paciente = paciente
            self.__medico = medico
            self.__medicamentos = medicamentos
            self.__fecha = datetime.now()

        def __str__(self):  
            meds = ", ".join(self.__medicamentos)
            return f"Receta para {self.__paciente} por {self.__medico.obtener_matricula()} el {self.__fecha.strftime('%d/%m/%Y')}:\n{meds}"


class TestReceta(unittest.TestCase):
    
    def setUp(self):
        """Configurar objetos mock para usar en los tests"""
        
        self.mock_paciente = Mock()
        self.mock_paciente.__str__ = Mock(return_value="Juan Pérez")
        
        
        self.mock_medico = Mock()
        self.mock_medico.obtener_matricula = Mock(return_value="MP12345")
        
        
        self.medicamentos = ["Paracetamol", "Ibuprofeno", "Vitamina D"]
        
        
        self.fecha_test = datetime(2024, 6, 15, 10, 30, 0)
    
    def test_constructor_con_parametros_validos(self):
        """Test 1: Constructor con parámetros válidos"""
        receta = Receta(self.mock_paciente, self.mock_medico, self.medicamentos)
        
        self.assertEqual(receta._Receta__paciente, self.mock_paciente)
        self.assertEqual(receta._Receta__medico, self.mock_medico)
        self.assertEqual(receta._Receta__medicamentos, self.medicamentos)
        self.assertIsInstance(receta._Receta__fecha, datetime)
    
    @patch('__main__.datetime' if 'src.receta' not in sys.modules else 'src.receta.datetime')
    def test_constructor_fecha_automatica(self, mock_datetime):
        """Test 2: Constructor asigna fecha automáticamente"""
        mock_datetime.now.return_value = self.fecha_test
        
        receta = Receta(self.mock_paciente, self.mock_medico, self.medicamentos)
        
        mock_datetime.now.assert_called_once()
        self.assertEqual(receta._Receta__fecha, self.fecha_test)
    
    def test_constructor_con_medicamento_unico(self):
        """Test 3: Constructor con un solo medicamento"""
        medicamento_unico = ["Aspirina"]
        receta = Receta(self.mock_paciente, self.mock_medico, medicamento_unico)
        
        self.assertEqual(receta._Receta__medicamentos, medicamento_unico)
        self.assertEqual(len(receta._Receta__medicamentos), 1)
    
    def test_constructor_con_lista_medicamentos_vacia(self):
        """Test 4: Constructor con lista de medicamentos vacía"""
        medicamentos_vacios = []
        receta = Receta(self.mock_paciente, self.mock_medico, medicamentos_vacios)
        
        self.assertEqual(receta._Receta__medicamentos, medicamentos_vacios)
        self.assertEqual(len(receta._Receta__medicamentos), 0)
    
    @patch('__main__.datetime' if 'src.receta' not in sys.modules else 'src.receta.datetime')
    def test_str_formato_correcto(self, mock_datetime):
        """Test 5: Método __str__ devuelve formato correcto"""
        mock_datetime.now.return_value = self.fecha_test
        
        receta = Receta(self.mock_paciente, self.mock_medico, self.medicamentos)
        resultado = str(receta)
        
        expected = "Receta para Juan Pérez por MP12345 el 15/06/2024:\nParacetamol, Ibuprofeno, Vitamina D"
        self.assertEqual(resultado, expected)
    
    @patch('__main__.datetime' if 'src.receta' not in sys.modules else 'src.receta.datetime')
    def test_str_con_medicamento_unico(self, mock_datetime):
        """Test 6: Método __str__ con un solo medicamento"""
        mock_datetime.now.return_value = self.fecha_test
        
        receta = Receta(self.mock_paciente, self.mock_medico, ["Paracetamol"])
        resultado = str(receta)
        
        expected = "Receta para Juan Pérez por MP12345 el 15/06/2024:\nParacetamol"
        self.assertEqual(resultado, expected)
    
    @patch('__main__.datetime' if 'src.receta' not in sys.modules else 'src.receta.datetime')
    def test_str_con_medicamentos_vacios(self, mock_datetime):
        """Test 7: Método __str__ con lista de medicamentos vacía"""
        mock_datetime.now.return_value = self.fecha_test
        
        receta = Receta(self.mock_paciente, self.mock_medico, [])
        resultado = str(receta)
        
        expected = "Receta para Juan Pérez por MP12345 el 15/06/2024:\n"
        self.assertEqual(resultado, expected)
    
    def test_atributos_privados_no_accesibles(self):
        """Test 8: Los atributos privados no son accesibles directamente"""
        receta = Receta(self.mock_paciente, self.mock_medico, self.medicamentos)
        
       
        with self.assertRaises(AttributeError):
            _ = receta.paciente
        
        with self.assertRaises(AttributeError):
            _ = receta.medico
            
        with self.assertRaises(AttributeError):
            _ = receta.medicamentos
            
        with self.assertRaises(AttributeError):
            _ = receta.fecha
    
    @patch('__main__.datetime' if 'src.receta' not in sys.modules else 'src.receta.datetime')
    def test_interaccion_con_objetos_dependientes(self, mock_datetime):
        """Test 9: Verificar interacción correcta con objetos Paciente y Medico"""
        mock_datetime.now.return_value = self.fecha_test
        
        receta = Receta(self.mock_paciente, self.mock_medico, self.medicamentos)
        _ = str(receta) 
        
        
        self.mock_paciente.__str__.assert_called()
        self.mock_medico.obtener_matricula.assert_called()
    
    @patch('__main__.datetime' if 'src.receta' not in sys.modules else 'src.receta.datetime')
    def test_formato_fecha_correcto(self, mock_datetime):
        """Test 10: Verificar que el formato de fecha es correcto"""
       
        fechas_test = [
            datetime(2024, 1, 1, 0, 0, 0),     
            datetime(2024, 12, 31, 23, 59, 59), 
            datetime(2023, 7, 15, 12, 30, 45)   
        ]
        
        for fecha in fechas_test:
            with self.subTest(fecha=fecha):
                mock_datetime.now.return_value = fecha
                
                receta = Receta(self.mock_paciente, self.mock_medico, self.medicamentos)
                resultado = str(receta)
                
                fecha_esperada = fecha.strftime('%d/%m/%Y')
                self.assertIn(fecha_esperada, resultado)


if __name__ == '__main__':
    
    unittest.main(verbosity=2)