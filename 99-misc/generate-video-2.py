import bpy
import pathlib
import os
import subprocess

OBJ_PATH = '/home/leoho/repos/pipeline/99-misc/data/002/'
# Adjust this for where you have the OBJ files.
obj_root = pathlib.Path(OBJ_PATH)

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

for obj_fname in obj_root.glob('*.obj'):
    bpy.ops.import_scene.obj(filepath=str(obj_fname))
    for i in bpy.context.visible_objects:
        print(i.data)
        # Use Phong smoothing for all meshes in scene
        mesh = i.data
        if hasattr(mesh, 'polygons'):
            print("Applying Phong smoothing to " + str(i.data))
            for f in mesh.polygons:
                f.use_smooth = True
    scene.render.filepath = f'{OBJ_PATH}/obj-{obj_fname.stem}'
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
command = ["ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4"]
subprocess.run(command)

print('ended')