import random
import time
import csv

class MockNeuroSkyDataCollector:
    """Clase Mock que nos ayuda a simular un dispositivo mindwave"""
    def __init__(self, signal_type="raw", save_to_csv=False, csv_file='mock_data.csv', graph=False):
        self.signal_type = signal_type
        self.save_to_csv = save_to_csv
        self.csv_file = csv_file
        self.graph = graph
        self.data = []
        self.is_collecting = False

    def connect(self):
        print(f"[Mock] Connected to simulated NeuroSky device for signal: {self.signal_type}")

    def collect_data(self, duration=10):
        print("[Mock] Collecting simulated data...")
        self.is_collecting = True
        start_time = time.time()

        while time.time() - start_time < duration:
            # Genera un dato simulado que varía según el tipo de señal
            value = random.uniform(0, 100) if self.signal_type in ["attention", "meditation"] else random.randint(-2048, 2048)
            self.data.append(value)
            print(f"[Mock] Generated value: {value}")  # Imprime el valor generado
            time.sleep(0.5)  # Simula un intervalo entre datos

        self.is_collecting = False
        print("[Mock] Data collection finished.")

    def print_data(self):
        print("[Mock] Printing collected data:")
        print(self.data)

    def animate_plot(self):
        # Este método simula la acción de graficar
        print("[Mock] Animating plot with collected data... (this is a mock)")

    def stop(self):
        self.is_collecting = False
        print("[Mock] Data collection stopped.")
