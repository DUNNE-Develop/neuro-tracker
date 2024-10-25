import csv
import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.neurosky_interface import NeuroSkyInterface

import threading

SAMPLE_FREQ = 512.0

        #DUNNE esta clase es la "MADRE" de todos los modules, por lo que es lo primero que deberiamos de modificar antes de 
        # entrar a la carpeta modules a la cual tambiens se le planean hacer cambios

        #Cambios futuros que se podrian hacer: como es un problema esepecifido podriamos hacer nuestra propia comunicacio serial,
        #hacer el lector de microvolts y calcular las formulas de atencion con la tranformada de fourier.

class NeuroSkyDataCollector:
    def __init__(self, sample_freq=SAMPLE_FREQ, port=None, signal_type='raw', graph=False, csv_file='data.csv', save_to_csv=True, use_mock=False):
        """
        Inicializa el recolector de datos del NeuroSky.
        :param sample_freq: Frecuencia de muestreo para la recolección de datos.
        :param port: Puerto serial al que está conectado el dispositivo NeuroSky.
        :param signal_type: Tipo de señal a recolectar ('raw', 'attention', 'meditation', etc.).
        :param graph: Si es True, se graficarán los datos en tiempo real.
        :param csv_file: Nombre del archivo CSV donde se guardarán los datos.
        :param save_to_csv: Si es True, se guardarán los datos en un archivo CSV.
        """
        self.port = port
        self.signal_type = signal_type
        self.graph = graph
        self.sample_freq = sample_freq
        self.raw_data = []
        self.running = False
        self.interface = None
        self.csv_file = csv_file
        self.save_to_csv = save_to_csv
        self.fig, self.ax, self.line = None, None, None
        self.data_thread = None  
        self.csv_writer = None  # Variable para manejar el archivo CSV
        self.csv_file_handle = None  # Manejador del archivo CSV
        self.use_mock = use_mock

    def connect(self):
        """
        Conectar al dispositivo NeuroSky o inicializar el mock.
        """
        try:
            if self.use_mock:
                # Usar el mock si `use_mock` es True
                self.interface = MockNeuroSkyInterface(self.port)
                print("Mock: Simulación de NeuroSky conectada.")
            else:
                if not self.port:
                    raise ValueError("El puerto serial no ha sido especificado.")
                self.interface = NeuroSkyInterface(self.port)
                print(f"Conectado a NeuroSky en el puerto {self.port}.")
        except Exception as e:
            print(f"Error de conexión: {e}")

    def collect_data(self):
        """
        Colecta datos usando el dispositivo o el mock.
        """
        if not self.interface:
            raise ValueError("No se ha establecido conexión con el dispositivo o mock.")
        
        self.running = True
        self.raw_data = []

        try:
            if self.save_to_csv:
                self.csv_file_handle = open(self.csv_file, mode='w', newline='')
                self.csv_writer = csv.writer(self.csv_file_handle)
                self.csv_writer.writerow(['Timestamp', self.signal_type.capitalize()])

            def collect():
                while self.running:
                    try:
                        if self.use_mock:
                            self.interface.update_mock_data()  # Generar datos mock
                        signal_value = self.get_signal_value(self.signal_type)
                        self.raw_data.append(signal_value)
                        if self.save_to_csv:
                            self.csv_writer.writerow([time.time(), signal_value])
                            self.csv_file_handle.flush()
                        if len(self.raw_data) > 512:
                            self.raw_data.pop(0)
                        time.sleep(1.0 / self.sample_freq)
                    except Exception as e:
                        print(f"Error durante la recolección de datos: {e}")
                        self.running = False

            self.data_thread = threading.Thread(target=collect)
            self.data_thread.start()

        except IOError as e:
            print(f"Error al abrir o escribir en el archivo CSV: {e}")
            self.running = False
        #DUNNE no entiendo por que el segundo parametero siempre es cero? PEROOO
        #de este codigo solo podriamos mandar a llamar directamente
        # self.interface.waves.get('attention', 0) para obtener el valor de attention directamente donde esto se este llamando a llamar
        # que es solo en el metodo collect_data() de esta misma clase
    def get_signal_value(self, signal_type):
        """
        Obtener el valor del tipo de señal especificado.
        :param signal_type: Tipo de señal a recolectar.
        :return: Valor de la señal especificada.
        """
        signal_mapping = {
            'raw': self.interface.raw_value,
            'attention': self.interface.attention,
            'meditation': self.interface.meditation,
            'blink': self.interface.blink,
            'delta': self.interface.waves.get('delta', 0),
            'theta': self.interface.waves.get('theta', 0),
            'low-alpha': self.interface.waves.get('low-alpha', 0),
            'high-alpha': self.interface.waves.get('high-alpha', 0),
            'low-beta': self.interface.waves.get('low-beta', 0),
            'high-beta': self.interface.waves.get('high-beta', 0),
            'low-gamma': self.interface.waves.get('low-gamma', 0),
            'mid-gamma': self.interface.waves.get('mid-gamma', 0)
        }
        return signal_mapping.get(signal_type, 0)


                #DUNNE esto detiene el hilo, no hay mucha ciencia, el hilo que se mantiene activo en la recoleccion de datos dice bye bye, mejor aqui si no le movemos
    def stop(self):
        """
        Detener la recolección de datos.
        """
        self.running = False
        if self.data_thread:
            self.data_thread.join()  
        if self.interface:
            self.interface.stop()
        if self.csv_file_handle:
            self.csv_file_handle.close()  # Cerrar el archivo CSV correctamente
        print("Recolección de datos detenida y archivo CSV cerrado.")


    #DUNNE initialiize_plot, update_plot y animate_plot son funciones que se encargan de graficar los datos en tiempo real usando
    #matplotlib.animation, tenemos la opcion de dejarlo asi como esta o cocinar en esta parte del codigo para solo mandar a llamar esta cosa, 
    #como opcion secundaria no eliminamos esta opcion pero empezamos a trabajar en la implementacion de una clase interfaz grafica mas bonita
    # para la interfaz grafica bonita observemos que esto funciona conu una lista de tuplas raw_data, que es lo que se recolecta en el hilo de recoleccion

    def initialize_plot(self):
        """
        Inicializar la gráfica para actualización en tiempo real.
        """
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_title(f"{self.signal_type.capitalize()} Data")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel(f"{self.signal_type.capitalize()} Value")
        self.ax.set_xlim(0, 512)
        self.ax.set_ylim(-2048, 2048)

    def update_plot(self, frame):
        """
        Actualizar los datos en la gráfica en tiempo real.
        """
        self.line.set_data(range(len(self.raw_data)), self.raw_data)
        self.ax.set_xlim(0, len(self.raw_data))
        return self.line,

    def animate_plot(self):
        """
        Graficar en tiempo real los datos recolectados.
        """
        if not self.raw_data:
            print("No hay datos para graficar.")
            return
        

        self.initialize_plot()
        ani = FuncAnimation(self.fig, self.update_plot, blit=True, interval=100)
        plt.show()

            #Esto imprime en terminal, duerme al hilo 1 seg quiero creer para que no estalle el pc, no se como funcionan los hilos y menos en python
            #pero yo creo que esta parte la podemos dejar asi u omirtirla ya que solo nos interesa la parte grafica
            #en el menu de seleccion solo seria necesario poner el tiempo de la prueba y el puerto COM3, ya que quique solo quiere que se muestrea attention

    def print_data(self):
        """
        Imprimir los datos recolectados en la consola.
        """
        while self.running:
            if self.raw_data:
                print(f"{self.signal_type.capitalize()} Value: {self.raw_data[-1]}")
            time.sleep(1.0 / self.sample_freq)

    def get_latest_data(self):
        """
        Obtener los datos más recientes recolectados.
        :return: Lista de valores de señal recolectados.
        """
        return self.raw_data

def validate_signal_type(signal_type):
    """
    Valida si el tipo de señal es válido.
    :param signal_type: Tipo de señal proporcionada por el usuario.
    :raises ValueError: Si el tipo de señal no es válido.
    """
    valid_signals = ['raw', 'attention', 'meditation', 'blink', 'delta', 'theta', 
                     'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 
                     'low-gamma', 'mid-gamma']

    if signal_type not in valid_signals:
        raise ValueError(f"Tipo de señal inválido: {signal_type}. Los tipos válidos son: {', '.join(valid_signals)}")


        #DUNNE tambien recomiendo separar el main de la clase y que esto solo se mande a llamar, que realmente es lo que hacen las pruebas
        #de neuro_tracker, pero este es un buen ejemplo de como la señal debe de ser tratada
        #las clases de  igual no deberian de ser cambiadas, ya que se encargan de la comunicacion con todo lo demas

