            #Recoleccion de Datos y almacenamiento en un archivo CSV

from neurosky_data_collector import NeuroSkyDataCollector

port = "COM3"
signal_type = "raw"

collector = NeuroSkyDataCollector(port = port, signal_type = signal_type, save_to_csv = True,
                                  csv_file = 'data.csv')
collector.connect()

#esta  linea de aqui crea el csv
collector.collect_data()

#Necesito vercuanto tiempo corre el programa
collector.stop()


            #Visualizar los datos en tiempo real

signal_type = "attention"
#Revisar los constructores de la clase NeuroSkyDataCollector
collector = NeuroSkyDataCollector(port = port, signal_type = signal_type, graph = True)
collector.connect()

collector.collect_data()

#Supongo que esta clase es la que imprime los datos usando la extension de matplotlib en tiempo rea
collector.animate_plot()


            #Imprimer los datos en terminal
signal_type = "meditation"
collector = NeuroSkyDataCollector(port = port, signal_type = signal_type,
                                  save_to_csv=False, graph=False)

collector.collect_data()
#Esto si imprime los valores en la consola.
collector.print_data()

#Ahora dando como buena la implementacion de la clase neurosky_data_collector.py
#podriamos solo modular este problema, en la cuals solo meteriamos mano a la clase animate_plot
#Esto es solo una idea pero este archivo no tiene la finalidad de ser ejecutado como main



