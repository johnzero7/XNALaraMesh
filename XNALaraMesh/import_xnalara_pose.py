# -*- coding: utf-8 -*-

from XNALaraMesh import read_ascii_xps
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

def getInputFilename(filename):

    blenderImportSetup()
    xpsImport(filename)
    blenderImportFinalize()

def blenderImportSetup():
    pass

def blenderImportFinalize():
    pass

def loadXpsFile(filename):
#    dirpath, file = os.path.split(filename)
#    basename, ext = os.path.splitext(file)
    xpsData = read_ascii_xps.readXpsPose(filename)

    return xpsData

@timing
def xpsImport(filename):
    global rootDir
    global xpsData

    print ("------------------------------------------------------------")
    print ("---------------EXECUTING XPS PYTHON IMPORTER----------------")
    print ("------------------------------------------------------------")
    print ("Importing Pose: ", filename)

    rootDir, file = os.path.split(filename)
    print ("rootDir: " + rootDir)

    xpsData = loadXpsFile(filename)

    pose_ob = importPose()

def importPose():
    boneCount = len(xpsData)
    print('Importing Pose', str(boneCount), 'bones')

    armature = next((obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE'), None)
    setXpsPose(armature, xpsData)

def resetPose(armature):
    for bone in armature.pose.bones:
        bone.matrix_basis = Matrix()

def setXpsPose(armature, xpsData):
    resetPose(armature)
    currentMode = bpy.context.mode
    currentObj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    scn = bpy.context.scene
    rigobj = armature
    arm = armature.data
    scn.objects.active = rigobj
    rigobj.select = True

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    for boneData in xpsData.items():
        xpsBoneData = boneData[1]
        boneName = xpsBoneData.boneName
        poseBone = rigobj.pose.bones.get(boneName)

        if poseBone:
            xpsPoseBone(poseBone, xpsBoneData)
    bpy.ops.object.posemode_toggle()
    scn.objects.active = currentObj
    bpy.ops.object.mode_set(mode=currentMode)

def xpsPoseBone(poseBone, xpsBoneData):
    xpsBoneRotate(poseBone, xpsBoneData.rotDelta)
    xpsBoneTranslate(poseBone, xpsBoneData.coordDelta)
    xpsBoneScale(poseBone, xpsBoneData.scale)

def xpsBoneRotToEuler(rotDelta):
    xRad = radians(rotDelta.x)
    yRad = radians(rotDelta.y)
    zRad = radians(rotDelta.z)
    return Euler((xRad, yRad, zRad),'YXZ')

def vectorTransform(vec):
    x = vec.x
    y = vec.y
    z = vec.z
    z = -z
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

def xpsBoneRotate(bone, rotDelta):
    rotation = vectorTransform(rotDelta)
    eulerRot = xpsBoneRotToEuler(rotation)
    origRot = bone.matrix.to_quaternion() #GLOBAL PoseBone

    rotation = eulerRot.to_quaternion()
    bone.rotation_mode = 'QUATERNION'
    bone.rotation_quaternion = origRot.inverted() * rotation * origRot

def xpsBoneTranslate(bone, coordsDelta):
    translate = vectorTransformTranslate(coordsDelta)
    bone.location = translate

def xpsBoneScale(bone, scale):
    newScale = vectorTransformScale(scale)
    bone.scale = newScale

if __name__ == "__main__":
    readPosefilename0 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili.pose'
    readPosefilename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 1.pose'
    readPosefilename2 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 2.pose'
    readPosefilename3 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 3.pose'
    readPosefilename4 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 4.pose'
    readPosefilename5 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 5.pose'
    readPosefilename6 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 6.pose'

    getInputFilename(readPosefilename6)



