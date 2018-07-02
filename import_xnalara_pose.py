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


PLACE_HOLDER = r'*side*'
RIGHT_BLENDER_SUFFIX = r'.R'
LEFT_BLENDER_SUFFIX = r'.L'
RIGHT_XPS_SUFFIX = r'right'
LEFT_XPS_SUFFIX = r'left'


def changeBoneNameToBlender(boneName, xpsSuffix, blenderSuffix):
    ''' '''
    #replace suffix with place holder
    newName = re.sub(xpsSuffix, PLACE_HOLDER, boneName, flags=re.I)
    #remove doble spaces
    newName = re.sub('\s+', ' ', newName, flags=re.I)
    newName = str.strip(newName)
    if boneName != newName:
        newName = '{0}{1}'.format(newName, blenderSuffix)

    return newName.strip()


def renameBoneToBlender(oldName):
    newName = oldName
    if PLACE_HOLDER not in oldName.lower():
        if re.search(LEFT_XPS_SUFFIX, oldName, flags=re.I):
            newName = changeBoneNameToBlender(oldName, LEFT_XPS_SUFFIX, LEFT_BLENDER_SUFFIX)

        if re.search(RIGHT_XPS_SUFFIX, oldName, flags=re.I):
            newName = changeBoneNameToBlender(oldName, RIGHT_XPS_SUFFIX, RIGHT_BLENDER_SUFFIX)

    return newName


def renameBonesToBlender(armatures_obs):
    currActive = bpy.context.active_object
    for armature in armatures_obs:
        for bone in armature.data.bones:
            bone.name = renameBoneToBlender(bone.name)


def changeBoneNameToXps(oldName, blenderSuffix, xpsSuffix):
    #remove '.R' '.L' from the end of the name
    newName = re.sub('{0}{1}'.format(re.escape(blenderSuffix), '$'), '', oldName, flags=re.I)
    #remove doble spaces
    newName = re.sub('\s+', ' ', newName, flags=re.I)
    #replcace place holder
    newName = re.sub(re.escape(PLACE_HOLDER), xpsSuffix, newName, flags=re.I)
    return newName


def renameBoneToXps(oldName):
    newName = oldName
    if PLACE_HOLDER in oldName.lower():
        if re.search(re.escape(LEFT_BLENDER_SUFFIX), oldName, re.I):
            newName = changeBoneNameToXps(oldName, LEFT_BLENDER_SUFFIX, LEFT_XPS_SUFFIX)

        if re.search(re.escape(RIGHT_BLENDER_SUFFIX), oldName, re.I):
            newName = changeBoneNameToXps(oldName, RIGHT_BLENDER_SUFFIX, RIGHT_XPS_SUFFIX)

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
    rigobj.select_set(action='SELECT')

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
