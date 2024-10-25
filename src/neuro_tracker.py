from modules.MockNeuroSkyDataCollector import MockNeuroSkyDataCollector
from neurosky_data_collector import NeuroSkyDataCollector, validate_signal_type

SAMPLE_FREQ = 512.0

def main(mock=False):
    try:
        # Obtener parámetros de entrada del usuario
        port = input("Especifica el puerto serial (ej. COM3 o /dev/ttyUSB0): ").strip()
        signal_type = input("Especifica el tipo de señal (ej. raw, attention): ").strip().lower()
        validate_signal_type(signal_type)

        graph = input("¿Quieres graficar los datos en tiempo real? (s/n): ").strip().lower() == 's'
        save_to_csv = input("¿Quieres guardar los datos en un archivo CSV? (s/n): ").strip().lower() == 's'
        csv_file = input("Especifica el nombre del archivo CSV (ej. data.csv): ").strip() if save_to_csv else ""

        # Usar Mock si está activado
        collector_class = MockNeuroSkyDataCollector if mock else NeuroSkyDataCollector

        # Crear y configurar el colector de datos
        collector = collector_class(SAMPLE_FREQ,port=port,signal_type=signal_type, graph=graph, csv_file=csv_file, save_to_csv=save_to_csv)
        collector.connect()  # Este es el método que deberías verificar

        # Recolectar y mostrar datos (con una duración específica)
        collector.collect_data()  # Asegúrate de que la duración sea suficiente
        if graph:
            collector.animate_plot()  # Asegúrate de que esto funcione con tu mock
        else:
            collector.print_data()  # Imprimir los datos recolectados

    except KeyboardInterrupt:
        print("Interrupción recibida, deteniendo recolección.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'collector' in locals():
            collector.stop()


if __name__ == "__main__":
    main()
