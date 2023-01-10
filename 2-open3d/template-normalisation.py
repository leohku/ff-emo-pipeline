import os
import trimesh
import math

def generate_output_path(BASE_DATA_PATH, input_path):
  subject_name = input_path.split(os.sep)[-2]
  output_path_dir = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER", "templates")
  output_path = os.path.join(output_path_dir, f"{subject_name}.obj")
  return output_path, output_path_dir

def template_normalisation_ind(input_path, output_path):
  mesh = trimesh.load(input_path)
  # Center the mesh
  mesh.vertices -= mesh.centroid
  # Normalise vertices by sqrt of total surface area
  mesh.vertices /= math.sqrt(mesh.area)
  mesh.export(output_path)

def do_template_normalisation(BASE_DATA_PATH):
  print("2-open3d: template-normalisation start")

  BASE_PATH_OPEN3D = os.path.join(BASE_DATA_PATH, "MEAD_OPEN3D")
  for root, dirs, files in os.walk(BASE_PATH_OPEN3D):
    for file in files:
      if file == "template.obj":
        input_path = os.path.join(root, file)
        output_path, output_path_dir = generate_output_path(BASE_DATA_PATH, input_path)
        # Create destination folder if not exist
        if not os.path.exists(output_path_dir):
          os.makedirs(output_path_dir)
          print(f"Output path {output_path_dir} created")
        template_normalisation_ind(input_path, output_path)
        print(f"Finished template normalisation for {input_path}, saved to {output_path}")

  print("2-open3d: template-normalisation end")

def main():
  BASE_DATA_PATH = "../test-data/"
  do_template_normalisation(BASE_DATA_PATH)

if __name__ == "__main__":
  main()