# -*- coding: utf-8 -*-

from XNALaraMesh import write_ascii_xps
from XNALaraMesh import xps_types

import bpy
import time
import os
import math
import mathutils
import re

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

def getOutputPoseSequence(filename):
    filepath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    poseSuffix = re.sub('\d+$', '', basename)
    
    startFrame = bpy.context.scene.frame_start
    endFrame = bpy.context.scene.frame_end
    initialFrame = bpy.context.scene.frame_current

    for currFrame in range(startFrame, endFrame+1):
        bpy.context.scene.frame_set(currFrame)
        numSuffix = '{:0>3d}'.format(currFrame)
        name = poseSuffix + numSuffix + ext
        
        newPoseFilename = os.path.join(filepath, name)
        getOutputFilename(newPoseFilename)

    bpy.context.scene.frame_current = initialFrame
        
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
    newVec = Vector((x, z, y))
    return newVec

def vectorTransformScale(vec):
    x = vec.x
    y = vec.y
    z = vec.z
    newVec = Vector((x, y, z))
    return newVec

def xpsBoneRotate(poseBone):
    poseMatGlobal = poseBone.matrix_basis.to_quaternion() #LOCAL PoseBone
    editMatLocal = poseBone.bone.matrix_local.to_quaternion() #LOCAL EditBoneRot

    rotQuat = editMatLocal * poseMatGlobal * editMatLocal.inverted()
    rotEuler = rotQuat.to_euler('YXZ')
    xpsRot = eulerToXpsBoneRot(rotEuler)
    rot = vectorTransform(xpsRot)
    return rot

def xpsBoneTranslate(poseBone):
    translate = poseBone.location
    editMatLocal = poseBone.bone.matrix_local.to_quaternion() #LOCAL EditBoneRot
    vector = editMatLocal * translate
    return vectorTransformTranslate(vector)

def xpsBoneScale(poseBone):
    scale = poseBone.scale
    return vectorTransformScale(scale)

if __name__ == "__main__":
    writePosefilename0 = r"G:\3DModeling\XNALara\XNALara_XPS\dataTest\Models\Queen's Blade\echidna pose - copy.pose"
    writePosefilename1 = r"G:\3DModeling\XNALara\XNALara_XPS\dataTest\Models\Queen's Blade\hide Kelta - copy.pose"

    getOutputFilename(writePosefilename1)


