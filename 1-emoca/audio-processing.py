import os
from pydub import AudioSegment


def generate_output_path(BASE_DATA_PATH, file_path):
  file_path_list = file_path.split(os.sep)
  # Get rid of the file extension
  file_path_list[-1] = file_path_list[-1].split(".")[0]
  p1, p2, p3, p4 = file_path_list[-5], file_path_list[-3], file_path_list[-2], file_path_list[-1]
  output_path = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER", "wav", f"{p1}_{p2}_{p3}_{p4}.wav")
  return output_path


def do_audio_processing(BASE_DATA_PATH):
  print("1-emoca: audio-processing start")

  # Create destination wav folder
  OUTPUT_PATH = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER", "wav")
  if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)
    print(f"Output path {OUTPUT_PATH} created")

  BASE_PATH_MEAD = os.path.join(BASE_DATA_PATH, "MEAD")
  for root, dirs, files in os.walk(BASE_PATH_MEAD):
    for file in files:
      if file.endswith(".m4a"):
        file_path = f"{root}/{file}"
        print(f"Processing {file_path}")
        output_path = generate_output_path(BASE_DATA_PATH, file_path)
        track = AudioSegment.from_file(file_path, format="m4a")
        track.export(output_path, format="wav")
        print(f"Converted wav to {output_path}")

  print("1-emoca: audio-processing end")


def main():
  BASE_DATA_PATH = "/home/leoho/repos/pipeline/test-data/"
  do_audio_processing(BASE_DATA_PATH)


if __name__ == "__main__":
  main()