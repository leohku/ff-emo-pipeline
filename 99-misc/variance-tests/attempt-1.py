import numpy as np
import matplotlib.pyplot as plt

# Read vertices from .obj
def extract_vert(filepath):
  with open(filepath, "r") as file:
      # Extract the vertex data from the file
      vertex_data = [line.split()[1:4] for line in file if line.startswith("v ")]
      vertex_array = np.array(vertex_data).astype(dtype="float32")
      return vertex_array

def get_data():
  # Load the .npy file (98, 15354)
  data = np.load("/home/leoho/repos/pipeline/test-data/MEAD_FACEFORMER/vertices_npy/M003_angry_level_1_001.npy")
  data_2 = np.load("/home/leoho/repos/pipeline/test-data/MEAD_FACEFORMER/vertices_npy/M003_angry_level_1_002.npy")
  data = np.concatenate((data, data_2), axis=0)
  print("Data Shape:", data.shape)
  # Load the template file (5118, 3)
  template_verts = extract_vert("/home/leoho/repos/pipeline/test-data/MEAD_FACEFORMER/templates/M003.obj")
  print("Template Shape:", template_verts.shape)

  processed_data = np.ndarray([data.shape[0], template_verts.shape[0]])

  for frame in range(0, data.shape[0]): # 98
    for vert in range(0, template_verts.shape[0]): # 5118
      # Read vert from template (5118, 3)
      template_vert = template_verts[vert]
      # Read vert from data (98, 15354)
      vert_x = data[frame, vert * 3]
      vert_y = data[frame, vert * 3 + 1]
      vert_z = data[frame, vert * 3 + 2]
      # Get Cartisian distance
      distance = np.sqrt((template_vert[0] - vert_x)**2 + (template_vert[1] - vert_y)**2 + (template_vert[2] - vert_z)**2)
      # Store distance in processed_data
      processed_data[frame, vert] = distance

  print(processed_data)
  print(processed_data.shape)
  return processed_data


def main():
  data = get_data()
  # Transpose to get vertice delta across time
  data = data.T
  print(data.shape)
  # Compute the FFT of the time-series data
  fft_data = np.fft.fft(data)

  # Compute the power spectral density (PSD) of the FFT data
  psd_data = np.abs(fft_data)**2 / len(fft_data)

  # Compute the frequency range of the FFT data
  freq = np.fft.fftfreq(len(fft_data[0]))

  # Plot the PSD of the FFT data
  plt.plot(freq, psd_data.T)
  plt.xlabel('Frequency')
  plt.ylabel('Power')
  plt.show()

if __name__ == "__main__":
  main()