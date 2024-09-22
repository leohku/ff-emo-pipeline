import numpy as np
import matplotlib.pyplot as plt

# Define the time series data
data = np.array([[0,1,2,1], [-1,0,1,0], [10,0,10,0]])

# Define the windowing function
hamming_window = np.hamming(data.shape[1])

# Apply the windowing function to the data
windowed_data = data * hamming_window

# Apply the Fast Fourier Transform to the windowed data
fft_data = np.fft.fft(windowed_data, axis=1)

# Compute the frequency spectrum
freq_spectrum = np.abs(fft_data)

# Plot the frequency spectrum
freqs = np.fft.fftfreq(data.shape[1], d=1)
print(freq_spectrum)
plt.plot(freqs, freq_spectrum.T)
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.show()
