import unittest
from unittest.mock import patch
from src.neuro_tracker import main  # Asegúrate de que este import sea correcto

class TestNeuroSkyDataCollector(unittest.TestCase):

    @patch('src.modules.MockNeuroSkyDataCollector.MockNeuroSkyDataCollector')
    def test_main_with_mock(self, mock_collector):
        mock_instance = mock_collector.return_value
        mock_instance.animate_plot.return_value = None

        # Simula el input del usuario
        with patch('builtins.input', side_effect=['/dev/ttyUSB0', 'attention', 'n', 'n']):
            main(mock=True)
        
        # Verifica que se llamaron los métodos esperados
        try:
            mock_instance.connect.assert_called_once()
            mock_instance.collect_data.assert_called_once_with(duration=10)  # Asegúrate de que esto coincida
            mock_instance.print_data.assert_called_once()
        except AssertionError as e:
            print(f"Error en la prueba: {e}")
            print(f"Conexiones realizadas: {mock_instance.connect.call_count}")
            raise

if __name__ == "__main__":
    unittest.main()
