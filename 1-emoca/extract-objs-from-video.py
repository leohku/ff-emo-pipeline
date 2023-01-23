import os
import subprocess
import shutil

def generate_output_path(BASE_DATA_PATH, file_path):
    fp = file_path.split(os.sep)
    # ['..', 'test-data', 'MEAD', 'M003', 'video-001', 'video', 'front', 'neutral', 'level_1', '002.mp4']
    fp[-1] = fp[-1].split(".")[0]
    subject_id, emotion, level, video_id = fp[-7], fp[-3], fp[-2], fp[-1]
    output_path = os.path.join(BASE_DATA_PATH, "MEAD_OPEN3D", subject_id, emotion, level, video_id)
    print(f'output path generated: {output_path}')
    return output_path

def run_emoca(input_path, EMOCA_OUTPUT_PATH):

    EMOCA_PY_PATH = './emoca/gdl_apps/EMOCA/demos/test_emoca_on_video.py'

    args = ['--input_video', input_path, '--output_folder', EMOCA_OUTPUT_PATH, '--model_name', 'EMOCA',
    '--save_mesh=True', '--save_images=False', '--save_codes=False']

    command = ['python', EMOCA_PY_PATH] + args
    print(f'Calling EMOCA on video {input_path}')
    subprocess.run(command)
    print(f'EMOCA finished.')
    
def do_extract_objs_from_video(BASE_DATA_PATH):
    print("1-emoca: extracting obj files from video start")

    EMOCA_OUTPUT_PATH = os.path.join(BASE_DATA_PATH, 'MEAD_EMOCA')

    for root, _, files in os.walk(os.path.join(BASE_DATA_PATH, 'MEAD')):
        for file in files:
            is_front_cam = len(root.split(os.sep)) >= 3 and root.split(os.sep)[-3] == "front"
            if file.endswith(".mp4") and is_front_cam:
                file_path = f"{root}/{file}"
                print(f"Processing {file_path}")
                run_emoca(file_path, EMOCA_OUTPUT_PATH)
                final_output_path = generate_output_path(BASE_DATA_PATH, file_path)
                if (not os.path.exists(final_output_path)):
                    os.makedirs(final_output_path)
                # dir generated: processed_2023_Jan_05_01-07-20/82-25-854x480_affwild2/results/EMOCA
                for dir in os.listdir(EMOCA_OUTPUT_PATH):
                    # 'mesh_coarse.obj' may exist in template_output - exclude MEAD_EMOCA/template_output
                    if dir != 'template_output':
                        for pp_root, _, pp_files in os.walk(os.path.join(EMOCA_OUTPUT_PATH, dir)):
                            for pp_file in pp_files:
                                if pp_file == 'mesh_coarse.obj':
                                    frame_count = pp_root.split(os.sep)[-1].split('_')[0] # extract the frame num from folder name
                                    print(f'Saving to {final_output_path}/mesh_coarse_{frame_count}.obj')
                                    pp_path = f'{pp_root}/{pp_file}'
                                    shutil.copy(pp_path, f'{final_output_path}/mesh_coarse_{frame_count}.obj')
                    # Delete output folder when processing done
                    if dir != 'template_output' and dir != 'template_input':
                        shutil.rmtree(os.path.join(EMOCA_OUTPUT_PATH, dir))
    
    print("1-emoca: extracting obj files from video end")

def main():
    BASE_DATA_PATH = os.environ["BASE_DATA_PATH"]
    do_extract_objs_from_video(BASE_DATA_PATH)

if __name__ == "__main__":
    main()
