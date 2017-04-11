import bpy
import os
import mathutils

basedir = 'C:/Users/nyou045/git/coronary_cfd_blender/'

# Clear Blender scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
print("scene cleared")

file = basedir + "arrow.fbx"
bpy.ops.import_scene.fbx(filepath=file)
o = bpy.context.selected_objects[0]
o.scale = (.1, .1, .1)
d = mathutils.Vector((1,1,1))
q = d.to_track_quat('Z','Y')
o.rotation_mode = 'QUATERNION'
o.rotation_quaternion = q
o.location = (0,0,0)

bpy.ops.object.duplicate()
o = bpy.context.selected_objects[0]
o.location = d