# Archivo: modules/mock_neurosky_interface.py
import random
import time

class MockNeuroSkyInterface:
    def __init__(self, port):
        self.port = port
        self.raw_value = 0
        self.attention = 0
        self.meditation = 0
        self.blink = 0
        self.waves = {
            'delta': 0,
            'theta': 0,
            'low-alpha': 0,
            'high-alpha': 0,
            'low-beta': 0,
            'high-beta': 0,
            'low-gamma': 0,
            'mid-gamma': 0
        }

    def update_mock_data(self):
        # Generar datos aleatorios para simular lecturas
        self.raw_value = random.randint(-2048, 2048)
        self.attention = random.randint(0, 100)
        self.meditation = random.randint(0, 100)
        self.blink = random.randint(0, 100)
        for key in self.waves:
            self.waves[key] = random.randint(0, 1000)
    
    def stop(self):
        print("Mock: Conexión cerrada.")
