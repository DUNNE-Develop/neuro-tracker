import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# Cargar los datos (suponiendo que ya tienes un archivo CSV)
data = pd.read_csv('data.csv')

# Convertir el tiempo en un formato legible si es necesario
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

# Función para diseñar un filtro Butterworth pasa-banda
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Función para aplicar un filtro pasa-banda
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return filtfilt(b, a, data)

# Asumir una frecuencia de muestreo (ajusta este valor según tu dispositivo)
fs = 512  # Por ejemplo, 512 Hz

# Filtrar las ondas alfa (8-12 Hz)
data['Alpha'] = bandpass_filter(data['Raw'], 8, 12, fs)

# Filtrar las ondas beta (12-30 Hz)
data['Beta'] = bandpass_filter(data['Raw'], 12, 30, fs)

# Graficar las señales filtradas
plt.figure(figsize=(14, 8))

# Graficar ondas Alfa
plt.subplot(2, 1, 1)
plt.plot(data['Timestamp'], data['Alpha'], color='g', linewidth=1)
plt.title('Ondas Alfa (8-12 Hz)')
plt.ylabel('Amplitud')
plt.xticks(rotation=45)

# Graficar ondas Beta
plt.subplot(2, 1, 2)
plt.plot(data['Timestamp'], data['Beta'], color='r', linewidth=1)
plt.title('Ondas Beta (12-30 Hz)')
plt.ylabel('Amplitud')
plt.xlabel('Tiempo')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
