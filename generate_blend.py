import bpy
import os
import mathutils
import csv
import copy
import glob
import re

basedir = '/home/nyou045/git/coronary_cfd_blender/'

# Clear Blender scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
print("scene cleared")

files = glob.glob(basedir + 'export-vel-time- *.csv')
files.sort()
print(files)
maxM = 0

scene = bpy.context.scene
# Keying Set Level declarations
ks = scene.keying_sets.new(idname="KeyingSet", name="LocRotScaleMat")

ks.use_insertkey_needed = False
ks.use_insertkey_visual = False
ks.use_insertkey_xyz_to_rgb = True

for file_index, f in enumerate(files):
    ts = int(re.search(r'export-vel-time- (\d+).csv', f).group(1)) - 405
    bpy.context.scene.frame_set(ts)
    print("tslice: {}".format(ts))
    with open(f) as fh:
        lines = fh.readlines()

    reader = list(csv.DictReader(lines[5:]))[::200]
    if file_index == 0: # initialise
        origin = None
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
            # offset to center
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
            ks.paths.add(o, 'location', index=-1)
            ks.paths.add(o, 'rotation_quaternion', index=-1)
            ks.paths.add(o, 'scale', index=-1)
            ks.paths.add(mat, 'diffuse_color', index=-1)
            bpy.ops.anim.keyframe_insert_menu()
    else:
        for i,r in enumerate(reader):
            if i % 100 == 0:
                print("loaded {}/{} points".format(i, len(reader)))
            o = bpy.data.objects[i]
            o.select = True
            p = mathutils.Vector((float(r[' X [ m ]']), float(r[' Y [ m ]']), float(r[' Z [ m ]'])))
            p -= origin
            d = mathutils.Vector((float(r[' Velocity u [ m s^-1 ]']), float(r[' Velocity v [ m s^-1 ]']), float(r[' Velocity w [ m s^-1 ]'])))
            m = d.magnitude
            if m > maxM:
                maxM = m

            q = d.to_track_quat('Z','Y')
            o.rotation_quaternion = q
            o.location = p
            o.scale = (m, m, m)
            color = mathutils.Color()
            color.hsv = (1-m/.15, 1, 1)
            o.active_material.diffuse_color = color
            bpy.ops.anim.keyframe_insert_menu()
            o.select = False

print("done - maxM: {}".format(maxM))
