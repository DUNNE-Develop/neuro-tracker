import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np

class BrainwaveProcessor:
    def __init__(self, sampling_frequency=512):
        self.sampling_frequency = sampling_frequency
        self.data_buffer = []  # Circular buffer of size 512
        self.buffer_size = 512
        self.timestamps = []
        self.alpha_data = []
        self.beta_data = []

    def _butter_bandpass(self, lowcut, highcut, order=4):
        nyquist = 0.5 * self.sampling_frequency
        low = lowcut / nyquist
        high = highcut / nyquist
        return butter(order, [low, high], btype='band')

    def _bandpass_filter(self, data, lowcut, highcut, order=4):
        b, a = self._butter_bandpass(lowcut, highcut, order=order)
        return filtfilt(b, a, data)

    def add_data_point(self, timestamp, raw_value):
        """Add a single data point to the circular buffer."""
        if len(self.data_buffer) >= self.buffer_size:
            self.data_buffer.pop(0)  # Remove the oldest data point
            self.timestamps.pop(0)

        self.data_buffer.append(raw_value)
        self.timestamps.append(timestamp)

    def has_sufficient_data(self):
        """Check if there are enough points to perform the analysis."""
        return len(self.data_buffer) == self.buffer_size

    def analyze_waves(self):
        """Analyze whether the current data set has more alpha or beta waves."""
        if not self.has_sufficient_data():
            return None

        # Filter for alpha (8-12 Hz) and beta (12-30 Hz)
        self.alpha_data = self._bandpass_filter(self.data_buffer, 8, 12)
        self.beta_data = self._bandpass_filter(self.data_buffer, 12, 30)

        # Calculate the mean power of each band
        alpha_power = np.mean(np.abs(self.alpha_data))
        beta_power = np.mean(np.abs(self.beta_data))

        if alpha_power > beta_power:
            return "Alpha Dominant"
        else:
            return "Beta Dominant"

    def plot_direct(self):
        """Plot the filtered alpha and beta waves from the current buffer."""
        if not self.has_sufficient_data():
            print("Not enough data to plot.")
            return

        plt.figure(figsize=(14, 8))

        # Plot Alpha waves
        plt.subplot(2, 1, 1)
        plt.plot(self.timestamps, self.alpha_data, color='g', linewidth=1)
        plt.title('Alpha Waves (8-12 Hz)')
        plt.ylabel('Amplitude')
        plt.xticks(rotation=45)

        # Plot Beta waves
        plt.subplot(2, 1, 2)
        plt.plot(self.timestamps, self.beta_data, color='r', linewidth=1)
        plt.title('Beta Waves (12-30 Hz)')
        plt.ylabel('Amplitude')
        plt.xlabel('Time')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def process_file(self, file_path):
        """Process and plot alpha and beta waves from a file."""
        data = pd.read_csv(file_path)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
        self.timestamps = data['Timestamp'].tolist()
        self.data_buffer = data['Raw'].tolist()

        if self.has_sufficient_data():
            # Filter for alpha (8-12 Hz) and beta (12-30 Hz)
            self.alpha_data = self._bandpass_filter(self.data_buffer, 8, 12)
            self.beta_data = self._bandpass_filter(self.data_buffer, 12, 30)
            self.plot_direct()


