import bpy
import os
import mathutils
import csv
import copy

basedir = 'C:/Users/nyou045/git/coronary_cfd_blender/'

# Clear Blender scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
print("scene cleared")

with open(basedir + 'export-new.csv') as f:
    lines = f.readlines()

reader = list(csv.DictReader(lines[5:]))[::200]
origin = None
count = 0;
maxM = 0;
for i,r in enumerate(reader):
    if i % 100 == 0:
        print("loaded {}/{} points".format(i, len(reader)))
    if not bpy.context.selected_objects:
        file = basedir + "arrow.fbx"
        print(file)
        bpy.ops.import_scene.fbx(filepath=file)
    else:
        bpy.ops.object.duplicate()
    o = bpy.context.selected_objects[0]
    p = mathutils.Vector((float(r[' X [ m ]']), float(r[' Y [ m ]']), float(r[' Z [ m ]'])))
    if i == 0:
        origin = copy.copy(p)
    p -= origin
    d = mathutils.Vector((float(r[' Velocity u [ m s^-1 ]']), float(r[' Velocity v [ m s^-1 ]']), float(r[' Velocity w [ m s^-1 ]'])))
    m = d.magnitude
    if m > maxM:
        maxM = m
    
    q = d.to_track_quat('Z','Y')
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = q
    o.location = p
    o.scale = (m, m, m)
    mat = bpy.data.materials.new("material")
    color = mathutils.Color()
    color.hsv = (1-m/.15, 1, 1)
    mat.diffuse_color = color
    o.active_material = mat

print("done - maxM: {}".format(maxM))