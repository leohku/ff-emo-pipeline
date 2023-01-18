import ffmpeg
import os
import shutil

def get_last_frame(video_path, output_path):
  (
    ffmpeg
    .input(video_path, sseof=-0.1)
    .output(output_path, vframes=1)
    .run(overwrite_output=True)
  )

def do_templates_creation(BASE_DATA_PATH):
  print("1-emoca: templates-creation start")

  # Create intermediate EMOCA folders
  EMOCA_INPUT_PATH = os.path.join(BASE_DATA_PATH, "MEAD_EMOCA", "template_input")
  EMOCA_OUTPUT_PATH = os.path.join(BASE_DATA_PATH, "MEAD_EMOCA", "template_output")
  if not os.path.exists(EMOCA_INPUT_PATH):
    os.mkdir(EMOCA_INPUT_PATH)
    print(f"Intermediate EMOCA input path {EMOCA_INPUT_PATH} created")
  if not os.path.exists(EMOCA_OUTPUT_PATH):
    os.mkdir(EMOCA_OUTPUT_PATH)
    print(f"Intermediate EMOCA output path {EMOCA_OUTPUT_PATH} created")

  BASE_PATH_MEAD = os.path.join(BASE_DATA_PATH, "MEAD")
  for dir in os.listdir(BASE_PATH_MEAD):
    # Create destination subject folder
    OUTPUT_PATH = os.path.join(BASE_DATA_PATH, "MEAD_OPEN3D", dir)
    if not os.path.exists(OUTPUT_PATH):
      os.mkdir(OUTPUT_PATH)
      print(f"Output path {OUTPUT_PATH} created")

    # Extract last frame from mp4
    file_path = os.path.join(BASE_PATH_MEAD, dir, "video-001", "video", "front", "neutral", "level_1", "001.mp4")
    extract_output_path = os.path.join(BASE_DATA_PATH, "MEAD_EMOCA", "template_input", f"{dir}.png")
    get_last_frame(file_path, extract_output_path)
    print(f"Saved last frame of {file_path} to {extract_output_path}")

  # Run EMOCA image mode
  emoca_image_script_path = os.path.abspath(os.path.join("/", "home", "leoho", "repos", "pipeline", "1-emoca", "emoca", "gdl_apps", "EMOCA", "demos", "test_emoca_on_images.py"))
  emoca_template_input_path = os.path.abspath(EMOCA_INPUT_PATH)
  emoca_template_output_path = os.path.abspath(EMOCA_OUTPUT_PATH)
  os.system(f"python {emoca_image_script_path} --input_folder {emoca_template_input_path} --output_folder {emoca_template_output_path} --model_name EMOCA --save_mesh=True")
  print(f"EMOCA image mode finished on all input images, saved to {EMOCA_OUTPUT_PATH}")

  # Put all output mesh_coarse.obj files to MEAD_OPEN3D folder
  for root, dirs, files in os.walk(EMOCA_OUTPUT_PATH):
    for file in files:
      if file == "mesh_coarse.obj":
        file_path_list = root.split(os.sep)
        # Remove last 00 from folder name
        file_path_list[-1] = file_path_list[-1][:-2]
        # Copy file to output folder
        copy_source = f"{root}{os.sep}{file}"
        copy_target = os.path.join(BASE_DATA_PATH, "MEAD_OPEN3D", file_path_list[-1], "template.obj")
        shutil.copy(copy_source, copy_target)
        print(f"Copied {copy_source} to {copy_target}")

  print("1-emoca: templates-creation end")

def main():
  BASE_DATA_PATH = os.environ["BASE_DATA_PATH"]
  do_templates_creation(BASE_DATA_PATH)

if __name__ == "__main__":
  main()