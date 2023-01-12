import os
import pickle
import trimesh

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
    mesh = trimesh.load(file_path)
    # Ensure the template vertices are of the correct shape
    print(f"shape: {mesh.vertices.shape}")
    if mesh.vertices.shape[0] != 59315 or mesh.vertices.shape[1] != 3:
      raise Exception("An obj doesn't have the exact number of vertices")

    templates[subject_name] = mesh.vertices.tolist()

  # Save templates dictionary
  f = open(os.path.join(BASE_PATH_FACEFORMER, "template.pkl"), "wb")
  pickle.dump(templates, f)

  print("3-preformer: template-packing end")

def main():
  BASE_DATA_PATH = "../test-data/"
  do_template_packing(BASE_DATA_PATH)

if __name__ == "__main__":
  main()