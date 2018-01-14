# -*- coding: utf-8 -*-
# <pep8 compliant>

from math import degrees
from math import radians
import math
import os
import re

from . import read_ascii_xps
from . import xps_types
from .timing import timing
import bpy
from mathutils import Euler
from mathutils import Matrix
from mathutils import Quaternion
from mathutils import Vector
import mathutils


def changeBoneName(boneName, suffix, replace):
    newName = re.sub(suffix, '*side*', boneName, 0, re.I)
    newName = re.sub(' +', ' ', newName, 0, re.I)
    newName = str.strip(newName)
    if boneName != newName:
        newName = '{}{}'.format(newName, replace)
    return newName.strip()


def renameBoneToBlender(oldName):
    newname = oldName
    suffix = 'left'
    if re.search(suffix, oldName, re.I):
        newname = changeBoneName(oldName, suffix, '.L')
    suffix = 'right'
    if re.search(suffix, oldName, re.I):
        newname = changeBoneName(oldName, suffix, '.R')
    return newname


def renameBonesToBlender(armatures_obs):
    currActive = bpy.context.active_object
    for armature in armatures_obs:
        for bone in armature.data.bones:
            bone.name = renameBoneToBlender(bone.name)


def renameBoneToXps(oldName):
    newName = oldName
    suffix = '\.L'
    if re.search(suffix, oldName, re.I):
        newName = re.sub(suffix, '', oldName, 0, re.I)
        newName = re.sub(' +', ' ', newName, 0, re.I)
        newName = re.sub('\*side\*', 'left', newName, 0, re.I)
    suffix = '\.R'
    if re.search(suffix, oldName, re.I):
        newName = re.sub(suffix, '', oldName, 0, re.I)
        newName = re.sub(' +', ' ', newName, 0, re.I)
        newName = re.sub('\*side\*', 'right', newName, 0, re.I)
    return newName.strip()


def renameBonesToXps(armatures_obs):
    for armature in armatures_obs:
        newName = ''
        for bone in armature.data.bones:
            bone.name = renameBoneToXps(bone.name)


def getInputPoseSequence(filename):
    filepath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    poseSuffix = re.sub('\d+$', '', basename)

    files = []
    for f in [file for file in os.listdir(filepath) if os.path.splitext(file)[1] == '.pose']:
        fName, fExt = os.path.splitext(f)
        fPoseSuffix = re.sub('\d+$', '', fName)
        if poseSuffix == fPoseSuffix:
            files.append(f)

    files.sort()

    initialFrame = bpy.context.scene.frame_current
    for poseFile in files:
        frame = bpy.context.scene.frame_current
        poseFilename = os.path.join(filepath, poseFile)
        importPoseAsKeyframe(poseFilename)
        bpy.context.scene.frame_current = frame + 1

    bpy.context.scene.frame_current = initialFrame


def importPoseAsKeyframe(filename):
    getInputFilename(filename)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.anim.keyframe_insert(type='LocRotScale')
    bpy.ops.object.mode_set(mode='OBJECT')


def getInputFilename(filename):

    blenderImportSetup()
    xpsImport(filename)
    blenderImportFinalize()


def blenderImportSetup():
    pass


def blenderImportFinalize():
    pass


def loadXpsFile(filename):
    # dirpath, file = os.path.split(filename)
    # basename, ext = os.path.splitext(file)
    xpsData = read_ascii_xps.readXpsPose(filename)

    return xpsData


@timing
def xpsImport(filename):
    global rootDir
    global xpsData

    print("------------------------------------------------------------")
    print("---------------EXECUTING XPS PYTHON IMPORTER----------------")
    print("------------------------------------------------------------")
    print("Importing Pose: ", filename)

    rootDir, file = os.path.split(filename)
    print("rootDir: " + rootDir)

    xpsData = loadXpsFile(filename)

    pose_ob = importPose()


def importPose():
    boneCount = len(xpsData)
    print('Importing Pose', str(boneCount), 'bones')

    armature = bpy.context.active_object
    setXpsPose(armature, xpsData)


def resetPose(armature):
    for poseBone in armature.pose.bones:
        poseBone.matrix_basis = Matrix()


def setXpsPose(armature, xpsData):
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
        if poseBone is None:
            poseBone = rigobj.pose.bones.get(renameBoneToBlender(boneName))

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
    return Euler((xRad, yRad, zRad), 'YXZ')


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
    z = -z
    newVec = Vector((x, z, y))
    return newVec


def vectorTransformScale(vec):
    x = vec.x
    y = vec.y
    z = vec.z
    newVec = Vector((x, y, z))
    return newVec


def xpsBoneRotate(poseBone, rotDelta):
    current_rottion_mode = poseBone.rotation_mode
    poseBone.rotation_mode = 'QUATERNION'
    rotation = vectorTransform(rotDelta)
    eulerRot = xpsBoneRotToEuler(rotation)
    origRot = poseBone.bone.matrix_local.to_quaternion()  # LOCAL EditBone

    rotation = eulerRot.to_quaternion()
    poseBone.rotation_quaternion = origRot.inverted() * rotation * origRot
    poseBone.rotation_mode = current_rottion_mode


def xpsBoneTranslate(poseBone, coordsDelta):
    translate = coordsDelta
    translate = vectorTransformTranslate(coordsDelta)
    origRot = poseBone.bone.matrix_local.to_quaternion()  # LOCAL EditBone

    poseBone.location = origRot.inverted() * translate


def xpsBoneScale(poseBone, scale):
    newScale = vectorTransformScale(scale)
    poseBone.scale = newScale

if __name__ == "__main__":
    readPosefilename1 = r"G:\3DModeling\XNALara\XNALara_XPS\dataTest\Models\Queen's Blade\hide Kelta.pose"

    getInputFilename(readPosefilename1)
