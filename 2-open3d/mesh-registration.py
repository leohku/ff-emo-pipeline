import os
import copy

import numpy as np
import open3d as o3d


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result


def mesh_registration_ind(template_path, file_path, output_path):
    voxel_size = 0.01
    print(":: Load two mesh.")
    target_mesh = o3d.io.read_triangle_mesh(template_path)
    source_mesh = o3d.io.read_triangle_mesh(file_path)

    print(":: Sample mesh to point cloud")
    target = copy.deepcopy(target_mesh).sample_points_uniformly(1000)
    source = copy.deepcopy(source_mesh).sample_points_uniformly(1000)

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    result_ransac = execute_global_registration(source_down, target_down,
                                                source_fpfh, target_fpfh,
                                                voxel_size)
    print(result_ransac)
    output_mesh = copy.deepcopy(source_mesh).transform(result_ransac.transformation)
    o3d.io.write_triangle_mesh(output_path, output_mesh)


def generate_output_and_template_path(BASE_DATA_PATH, file_path):
    file_path_list = file_path.split(os.sep)
    # Generate output path
    output_path_list = copy.deepcopy(file_path_list)
    output_path_list[-6] = "MEAD_PREFORMER"
    output_path = os.path.join(*output_path_list)
    output_path_dir = os.path.join(*output_path_list[:-1])
    # Generate template path
    template_path = os.path.join(BASE_DATA_PATH, "MEAD_PREFORMER", file_path_list[-5], "template.obj")
    return output_path, output_path_dir, template_path


def do_mesh_registration(BASE_DATA_PATH):
  print("2-open3d: mesh-registration start")

  BASE_PATH_OPEN3D = os.path.join(BASE_DATA_PATH, "MEAD_OPEN3D")
  for root, dirs, files in os.walk(BASE_PATH_OPEN3D):
    for file in files:
        if file.endswith(".obj"):
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
  BASE_DATA_PATH = "../test-data/"
  do_mesh_registration(BASE_DATA_PATH)

if __name__ == '__main__':
    main()