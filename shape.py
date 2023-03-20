import numpy as np

# Load the .npy file
data = np.load("/home/leoho/repos/pipeline/test-data/MEAD_FACEFORMER/vertices_npy/M003_angry_level_1_001.npy")

# Print the shape of the loaded data
print("Data Shape:", data.shape)
print("Data Shape after memory tweak:", (data[::2,:]).shape)