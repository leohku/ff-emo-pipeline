import numpy as np

# Define the time series data
data = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])

# Define the windowing function
hamming_window = np.hamming(data.shape[1])

# Apply the windowing function to the data
windowed_data = data * hamming_window

# Apply the Fast Fourier Transform to the windowed data
fft_data = np.fft.fft(windowed_data, axis=1)

# Compute the frequency spectrum
freq_spectrum = np.abs(fft_data)

# Set the frequency threshold
# threshold = 5.0

# Classify the vertices into high-frequency or low-frequency
# high_freq_vertices = np.where(freq_spectrum > threshold)[0]
# low_freq_vertices = np.where(freq_spectrum <= threshold)[0]

# print("High-frequency vertices:", high_freq_vertices)
# print("Low-frequency vertices:", low_freq_vertices)
