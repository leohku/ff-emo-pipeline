import numpy as np
import pickle
import matplotlib.pyplot as plt

# M003
# 230
# template_path = './data/M003.obj'
# clip_1_path = './data/M003_angry_level_1_001.npy'
# clip_2_path = './data/M003_angry_level_1_002.npy'

# M005
template_path = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/templates/M005.obj'
clip_1_path = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/vertices_npy/M005_contempt_level_3_019.npy'
clip_2_path = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/vertices_npy/M005_contempt_level_3_020.npy'

# W011
# 230
# template_path = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/templates/W011.obj'
# clip_1_path = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/vertices_npy/W011_neutral_level_1_001.npy'
# clip_2_path = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/vertices_npy/W011_neutral_level_1_002.npy'

# Objective: get 900 vertices' index with max variance

def read_template_obj_as_np(filepath):
  with open(filepath, "r") as file:
      # Extract the vertex data from the file
      vertex_data = [line.split()[1:4] for line in file if line.startswith("v ")]
      vertex_array = np.array(vertex_data).astype(dtype="float32")
      return vertex_array


def main():
    # prepare data
    clip_1 = np.load(clip_1_path)
    clip_2 = np.load(clip_2_path)

    input_clip = np.concatenate([clip_1, clip_2], axis=0)
    print(clip_1.shape)
    print(clip_2.shape)
    print('overall input clip shape', input_clip.shape)

    template = read_template_obj_as_np(template_path)
    template = template.flatten()
    print('template shape', template.shape)

    # calculate the distance from obj
    frame_num = input_clip.shape[0]
    vertex_start = input_clip.shape[1] // 3
    final = np.zeros((frame_num, vertex_start))
    
    for i in range(frame_num):
        frame = input_clip[i]
        # print(frame.shape)
        for j in range(0, vertex_start):
            x = j*3
            y = j*3 + 1
            z = j*3 + 2
            dist =  np.sqrt(((template[x] - frame[x]) ** 2 +
                    (template[y] - frame[y]) ** 2 +
                    (template[z] - frame[z]) ** 2))
            final[i][j] = dist
    
    print(final)
    print(final.shape)

    # find variance
    var = np.var(final, axis=0)
    var_sorted = np.sort(var)
    print(var_sorted.shape)
    plt.plot(var_sorted[:])
    plt.show()
    threshold = var_sorted[-901]

    # find the indexes of the vertices with variance > threshold
    indexes = np.where(var > threshold)
    print(indexes[0])
    # indexes[0] length = 900
    variance_indices = {}
    variance_indices['M005'] = indexes[0]

    f = open('variance_indices.pkl', 'wb')
    pickle.dump(variance_indices, f)

main()