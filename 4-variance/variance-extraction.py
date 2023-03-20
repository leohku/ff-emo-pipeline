import os
import numpy as np
import pickle

def read_template_obj_as_np(filepath):
  with open(filepath, "r") as file:
      # Extract the vertex data from the file
      vertex_data = [line.split()[1:4] for line in file if line.startswith("v ")]
      vertex_array = np.array(vertex_data).astype(dtype="float32")
      return vertex_array


def gen_paths_for(subject, faceformer_path):
    template_path = f"{faceformer_path}/templates/{subject}.obj"
    clip_1_path = f"{faceformer_path}/vertices_npy/{subject}_angry_level_3_001.npy"
    clip_2_path = f"{faceformer_path}/vertices_npy/{subject}_angry_level_3_002.npy"
    return template_path, clip_1_path, clip_2_path


def find_high_variance_indices(clip_1_path, clip_2_path, template_path):
    # prepare data
    clip_1 = np.load(clip_1_path)
    clip_2 = np.load(clip_2_path)
    input_clip = np.concatenate([clip_1, clip_2], axis=0)
    template = read_template_obj_as_np(template_path)
    template = template.flatten()

    # calculate the distance from obj
    frame_num = input_clip.shape[0]
    vertex_start = input_clip.shape[1] // 3
    final = np.zeros((frame_num, vertex_start))
    
    for i in range(frame_num):
        frame = input_clip[i]
        for j in range(0, vertex_start):
            x = j*3
            y = j*3 + 1
            z = j*3 + 2
            dist =  np.sqrt(((template[x] - frame[x]) ** 2 +
                    (template[y] - frame[y]) ** 2 +
                    (template[z] - frame[z]) ** 2))
            final[i][j] = dist
    
    # find variance
    var = np.var(final, axis=0)
    var_sorted = np.sort(var)
    threshold = var_sorted[-901]

    # find the indexes of the vertices with variance > threshold
    indexes = np.where(var > threshold)
    return indexes[0]


def do_variance_extraction(BASE_DATA_PATH):
    print("4-variance: variance-extraction start")

    BASE_PATH_FACEFORMER = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER")

    variance_indices = {}

    for subject in os.listdir(os.path.join(BASE_PATH_FACEFORMER, "templates")):
        subject = subject.split(".")[0]
        print("Processing subject:", subject)
        template_path, clip_1_path, clip_2_path = gen_paths_for(subject, BASE_PATH_FACEFORMER)
        high_variance_indices = find_high_variance_indices(clip_1_path, clip_2_path, template_path)
        if (len(high_variance_indices) != 900):
            raise Exception("The number of high variance indices is not 900 for subject: " + subject)
        variance_indices[subject] = high_variance_indices
    
    with open(os.path.join(BASE_PATH_FACEFORMER, "variance_indices.pkl"), "wb") as file:
        pickle.dump(variance_indices, file)

    print("4-variance: variance-extraction end")


def main():
    BASE_DATA_PATH = os.environ["BASE_DATA_PATH"]
    do_variance_extraction(BASE_DATA_PATH)


if __name__ == "__main__":
   main()