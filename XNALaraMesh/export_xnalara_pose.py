# -*- coding: utf-8 -*-

from XNALaraMesh import write_ascii_xps
from XNALaraMesh import xps_types

import time
import bpy
import os
import math
import mathutils

from mathutils import Euler
from mathutils import Quaternion
from mathutils import Vector
from mathutils import Matrix
from math import radians
from math import degrees

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def getOutputFilename(filename):

    blenderExportSetup()
    xpsExport(filename)
    blenderExportFinalize()

def blenderExportSetup():
    pass

def blenderExportFinalize():
    pass

def saveXpsFile(filename, xpsPoseData):
#    dirpath, file = os.path.split(filename)
#    basename, ext = os.path.splitext(file)
    write_ascii_xps.writeXpsPose(filename, xpsPoseData)

@timing
def xpsExport(filename):
    global rootDir
    global xpsData

    print ("------------------------------------------------------------")
    print ("---------------EXECUTING XPS PYTHON EXPORTER----------------")
    print ("------------------------------------------------------------")
    print ("Exporting Pose: ", filename)

    rootDir, file = os.path.split(filename)
    print ("rootDir: " + rootDir)

    xpsPoseData = exportPose()

    saveXpsFile(filename, xpsPoseData)

def exportPose():
    armature = next((obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE'), None)
    boneCount = len(armature.data.bones)
    print('Exporting Pose', str(boneCount), 'bones')

    return xpsPoseData(armature)

def xpsPoseData(armature):
    scn = bpy.context.scene
    currentMode = bpy.context.mode
    currentObj = bpy.context.active_object
    scn.objects.active = armature
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    bones = armature.pose.bones

    xpsPoseData = {}
    for poseBone in bones:
        boneName = poseBone.name
        boneData = xpsPoseBone(poseBone)
        xpsPoseData[boneName] = boneData

    bpy.ops.object.posemode_toggle()
    scn.objects.active = currentObj
    bpy.ops.object.mode_set(mode=currentMode)

    return xpsPoseData

def xpsPoseBone(poseBone):
    boneName = poseBone.name
    boneRotDelta = xpsBoneRotate(poseBone)
    boneCoordDelta = xpsBoneTranslate(poseBone)
    boneScale = xpsBoneScale(poseBone)
    boneData = xps_types.XpsBonePose(boneName, boneCoordDelta, boneRotDelta, boneScale)
    return boneData

def eulerToXpsBoneRot(rotEuler):
    xDeg = degrees(rotEuler.x)
    yDeg = degrees(rotEuler.y)
    zDeg = degrees(rotEuler.z)
    return Vector((xDeg, yDeg, zDeg))

def vectorTransform(vec):
    x = vec.x
    y = vec.y
    z = vec.z
    y = -y
    newVec = Vector((x, z, y))
    return newVec

def vectorTransformTranslate(vec):
    x = vec.x
    y = vec.y
    z = vec.z
    y = -y
    z = -z
    newVec = Vector((x, y, z))
    return newVec

def vectorTransformScale(vec):
    x = vec.x
    y = vec.y
    z = vec.z
    newVec = Vector((x, y, z))
    return newVec

def xpsBoneRotate(bone):
    poseMatGlobal = bone.matrix_basis.to_quaternion() #LOCAL PoseBone
    editMatLocal = bone.bone.matrix_local.to_quaternion() #LOCAL EditBoneRot

    rotQuat = editMatLocal * poseMatGlobal * editMatLocal.inverted()
    rotEuler = rotQuat.to_euler('YXZ')
    xpsRot = eulerToXpsBoneRot(rotEuler)
    rot = vectorTransform(xpsRot)
    return rot

def xpsBoneTranslate(bone):
    translate = bone.location
    return vectorTransformTranslate(translate)

def xpsBoneScale(bone):
    scale = bone.scale
    return vectorTransformScale(scale)

if __name__ == "__main__":
    writePosefilename0 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 0-ex.pose'
    writePosefilename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 1-ex.pose'
    writePosefilename2 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 2-ex.pose'
    writePosefilename3 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 3-ex.pose'
    writePosefilename4 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 4-ex.pose'
    writePosefilename5 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 5-ex.pose'
    writePosefilename6 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 6-ex.pose'

    getOutputFilename(writePosefilename5)


