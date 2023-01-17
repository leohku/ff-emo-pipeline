import os
import copy

import numpy as np
import open3d as o3d
import math

def mesh_registration_ind(template_path, file_path, output_path):
  input_mesh = o3d.io.read_triangle_mesh(file_path)

  # Move source_mesh to the center
  # input_mesh.translate(np.array([0,0,0]), relative=False)
  # Scale mesh to the sqrt of its surface area
  sqrt_surface_area = math.sqrt(input_mesh.get_surface_area())
  input_mesh.scale(1/sqrt_surface_area, np.array([0,0,0]))

  o3d.io.write_triangle_mesh(output_path, input_mesh)


def generate_output_and_template_path(BASE_DATA_PATH, file_path):
    file_path_list = file_path.split(os.sep)
    # Generate output path
    output_path_list = copy.deepcopy(file_path_list)
    output_path_list[-6] = "MEAD_PREFORMER"
    output_path = os.path.join(*output_path_list)
    output_path_dir = os.path.join(*output_path_list[:-1])
    # Generate template path
    template_path = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER", "templates", f"{file_path_list[-5]}.obj")
    return output_path, output_path_dir, template_path


def do_mesh_registration(BASE_DATA_PATH):
  print("2-open3d: mesh-registration start")

  BASE_PATH_OPEN3D = os.path.join(BASE_DATA_PATH, "MEAD_OPEN3D")
  for root, dirs, files in os.walk(BASE_PATH_OPEN3D):
    for file in files:
        if file.endswith(".obj") and file != "template.obj":
            file_path = f"{root}/{file}"
            print(f"Processing {file_path}")
            output_path, output_path_dir, template_path = generate_output_and_template_path(BASE_DATA_PATH, file_path)
            # Create destination folder if not exist
            if not os.path.exists(output_path_dir):
                os.makedirs(output_path_dir)
                print(f"Output path {output_path_dir} created")
            mesh_registration_ind(template_path, file_path, output_path)
            print(f"Finished registration for {file_path} with template {template_path}, saved to {output_path}")

  print("2-open3d: mesh-registration end")

def main():
  BASE_DATA_PATH = "/home/leoho/repos/pipeline/test-data/"
  do_mesh_registration(BASE_DATA_PATH)

if __name__ == '__main__':
    main()