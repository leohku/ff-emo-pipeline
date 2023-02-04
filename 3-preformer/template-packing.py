import os
import pickle
import numpy as np

def extract_vert(filepath):
  with open(filepath, "r") as file:
      # Extract the vertex data from the file
      vertex_data = [line.split()[1:4] for line in file if line.startswith("v ")]
      vertex_array = np.array(vertex_data).astype(dtype="float32")
      return vertex_array

def do_template_packing(BASE_DATA_PATH):
  print("3-preformer: template-packing start")

  templates = {}

  BASE_PATH_FACEFORMER = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER")
  for file in os.listdir(os.path.join(BASE_PATH_FACEFORMER, "templates")):
    file_path = os.path.join(BASE_PATH_FACEFORMER, "templates", file)
    print("Processing " + file_path, end=", ")
    # Get rid of file extension
    subject_name = file.split(".")[0]
    # Load vertices list
    verts = extract_vert(file_path)

    # Ensure the template vertices are of the correct shape
    print(f"shape: {verts.shape}")
    if verts.shape[0] != 5118 or verts.shape[1] != 3:
      raise Exception("An obj doesn't have the exact number of vertices")

    # Fix BUG-4: Outputs should be in np.ndarray format
    templates[subject_name] = verts

  # Save templates dictionary
  f = open(os.path.join(BASE_PATH_FACEFORMER, "template.pkl"), "wb")
  pickle.dump(templates, f)

  print("3-preformer: template-packing end")

def main():
  BASE_DATA_PATH = os.environ["BASE_DATA_PATH"]
  do_template_packing(BASE_DATA_PATH)

if __name__ == "__main__":
  main()