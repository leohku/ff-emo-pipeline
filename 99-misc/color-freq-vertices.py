import bpy
import pathlib
import os
import subprocess
import numpy as np

OBJ_PATH = '/home/leoho/data/pipeline-data/processed-data-faceformer/omnibus/templates/W014.obj'
# Adjust this for where you have the OBJ files.
# obj_root = pathlib.Path(OBJ_PATH)

# Before we start, make sure nothing is selected. The importer will select
# imported objects, which allows us to delete them after rendering.
bpy.ops.object.select_all(action='DESELECT')
scene = bpy.context.scene

scene.render.resolution_x = 2048
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.film_transparent = False

cam = scene.objects['Camera']
cam.location = (0.1, -1, 0)
cam.data.lens = 50
cam.data.sensor_width = 100


light = bpy.data.lights['Light']
light.type = 'POINT'
light.use_shadow = False
light.specular_factor = 3.0
light.diffuse_factor = 10
light.volume_factor = 20
light.energy = 100.0

# Add another light source so stuff facing away from light is not completely dark
bpy.ops.object.light_add(type='SUN')
light2 = bpy.data.lights['Sun']
light2.use_shadow = False
light2.specular_factor = 1.0
light2.energy = 4

cam_constraint = cam.constraints.new(type='TRACK_TO')
cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
cam_constraint.up_axis = 'UP_Y'
cam_empty = bpy.data.objects.new("Empty", None)
cam_empty.location = (0, 0, 0)
cam_constraint.target = cam_empty
cam.parent = cam_empty
# scene.collection.objects.link(cam_empty)
# bpy.context.view_layer.objects.active = cam_empty

# Remove the default cube layer at the back
objs = bpy.data.objects
objs.remove(objs["Cube"], do_unlink=True)
# scene.render.engine = 'CYCLES'

# for obj_fname in obj_root.glob('*.obj'):
bpy.ops.import_scene.obj(filepath=OBJ_PATH)

# Method of chatGPT
# print('000', bpy.data.objects['mesh_coarse_000001'])
# mesh = bpy.data.objects['mesh_coarse_000001']
# mesh_data = mesh.data
# vertex_colors = mesh_data.vertex_colors.new(name="colored-vertices")
# # for vert in selected_vertices:
# for idx, v in enumerate(mesh_data.vertices):
#     # print(idx, v)
#     vertex_colors.data[v.index].color = (1.0, 0.0, 0.0, 1.0) 

# mesh.update()
# print('mesh_data', mesh_data.vertices)
# print('mesh_data', mesh_data)
# print('1245')

# Method of obj files
# obj = bpy.context.selected_objects[0]

# mat = bpy.data.materials.new(name="New Material")
# mat.diffuse_color = (1, 0, 0, 1)

# # Assign material to object
# obj.data.materials.append(mat)

# # Export object as new OBJ file with color applied
# bpy.ops.export_scene.obj(filepath="./color-output/test1.obj")





# Method of gpt-4
mesh_obj = bpy.context.selected_objects[0]
mesh = mesh_obj.data

if not mesh.vertex_colors:
    mesh.vertex_colors.new()
vertex_colors = mesh.vertex_colors.active

def set_vertex_color(vertex_indices, color):
    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            loop = mesh.loops[loop_index]
            vertex_index = loop.vertex_index
            if vertex_index in vertex_indices:
                vertex_colors.data[loop_index].color = color
                print('loop_index', loop_index, vertex_colors, vertex_index)

vertex_indices = [i for i in range(500)]
color = (1.0, 0.0, 0.0, 1.0)
set_vertex_color(vertex_indices, color)

# Create a new material
material = bpy.data.materials.new(name="VertexColorMaterial")

# Enable 'Use Nodes'
material.use_nodes = True

# Assign the material to the mesh object
mesh.materials.clear()
mesh.materials.append(material)

# Get the material nodes
nodes = material.node_tree.nodes
links = material.node_tree.links

# Clear all existing nodes
nodes.clear()

# Create the necessary nodes
output_node = nodes.new(type="ShaderNodeOutputMaterial")
vertex_color_node = nodes.new(type="ShaderNodeVertexColor")
diffuse_bsdf_node = nodes.new(type="ShaderNodeBsdfDiffuse")

# Set the active vertex color layer as the input for the Vertex Color node
vertex_color_node.layer_name = vertex_colors.name

# Connect the nodes
links.new(vertex_color_node.outputs["Color"], diffuse_bsdf_node.inputs["Color"])
links.new(diffuse_bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

for i in bpy.context.visible_objects:
    print(i.data)
    # Use Phong smoothing for all meshes in scene
    mesh = i.data
    if hasattr(mesh, 'polygons'):
        print("Applying Phong smoothing to " + str(i.data))
        for f in mesh.polygons:
            f.use_smooth = True
scene.render.filepath = f'./color-output/test1.png'
bpy.ops.render.render(write_still=True)

# Remember which meshes were just imported
meshes_to_remove = []
for ob in bpy.context.selected_objects:
    meshes_to_remove.append(ob.data)

bpy.ops.object.delete()

# Remove the meshes from memory too
for mesh in meshes_to_remove:
    bpy.data.meshes.remove(mesh)


# TODO: need to cd to the directory
# command = ["ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4"]
# subprocess.run(command)

print('ended')