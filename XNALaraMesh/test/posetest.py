import bpy
import math
import mathutils

from math import *
from mathutils import *

def toDeg(euler):
    x=degrees(euler.x)
    y=degrees(euler.y)
    z=degrees(euler.z)
    return Vector((x,y,z))

poseBone = bpy.context.active_pose_bone

poseMatLocal = poseBone.matrix.copy() #GLOBAL
poseMatGlobal = poseBone.matrix_basis.copy() #LOCAL

matGlobal = poseBone.bone.matrix.copy() #GLOBAL
matLocal = poseBone.bone.matrix_local.copy() #LOCAL EditBoneRot

#mat_basis , matLocal NO MODIF
#mat , matLocal NO MODIF
#mat_basis , matGlobal NO MODIF
#mat , matGlobal NO MODIF

## variables
poseMatLocal = bpy.context.active_pose_bone.matrix.copy() #GLOBAL l
poseMatGlobal = bpy.context.active_pose_bone.matrix_basis.copy() #LOCAL
matGlobal = bpy.context.active_pose_bone.bone.matrix.copy() #GLOBAL 
matLocal = bpy.context.active_pose_bone.bone.matrix_local.copy() #LOCAL EditBoneRot

##posiciones
bpy.context.active_pose_bone.rotation_quaternion = matLocal.to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = matGlobal.to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = poseMatLocal.to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = poseMatGlobal.to_quaternion()

## ROTA 50 Z QUATERNION
bpy.context.active_pose_bone.rotation_quaternion = (matLocal.inverted() * Euler((pi/4.5,pi/7.2,pi/7.2),'YXZ').to_matrix().to_4x4() * matLocal).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (matGlobal.inverted() * Euler((pi/4.5,pi/7.2,pi/7.2),'YXZ').to_matrix() * matGlobal).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (poseMatLocal.inverted() * Euler((pi/4.5,pi/7.2,pi/7.2),'YXZ').to_matrix().to_4x4() * poseMatLocal).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (poseMatGlobal.inverted() * Euler((pi/4.5,pi/7.2,pi/7.2),'YXZ').to_matrix().to_4x4() * poseMatGlobal).to_quaternion()

## ROTA 50 Z MATRIX GLOBAL
bpy.context.active_pose_bone.matrix = (matLocal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * matLocal.to_3x3()).to_4x4()
bpy.context.active_pose_bone.matrix = (matGlobal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * matGlobal.to_3x3()).to_4x4()
bpy.context.active_pose_bone.matrix = (poseMatLocal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * poseMatLocal.to_3x3()).to_4x4()
bpy.context.active_pose_bone.matrix = (poseMatGlobal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * poseMatGlobal.to_3x3()).to_4x4()

## ROTA 50 Z MATRIX_BASIS LOCAL
bpy.context.active_pose_bone.matrix_basis = (matLocal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * matLocal.to_3x3()).to_4x4()
bpy.context.active_pose_bone.matrix_basis = (matGlobal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * matGlobal.to_3x3()).to_4x4()
bpy.context.active_pose_bone.matrix_basis = (poseMatLocal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * poseMatLocal.to_3x3()).to_4x4()
bpy.context.active_pose_bone.matrix_basis = (poseMatGlobal.inverted().to_3x3() * Euler((0,0,pi/4),'YXZ').to_matrix().to_3x3() * poseMatGlobal.to_3x3()).to_4x4()

##
bpy.context.active_pose_bone.rotation_quaternion = (matGlobal.inverted() * poseMatGlobal).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (matLocal.inverted().to_4x4() * poseMatLocal).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (matGlobal.inverted() * poseMatLocal.to_3x3() ).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (poseMatGlobal.to_4x4() * poseMatGlobal.inverted()).to_quaternion()

bpy.context.active_pose_bone.rotation_quaternion = (matGlobal.inverted() * matLocal.to_3x3()).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (matGlobal.inverted()).to_quaternion()
bpy.context.active_pose_bone.rotation_quaternion = (matLocal.to_3x3()).to_quaternion()

bpy.context.active_pose_bone.rotation_quaternion = (matGlobal * poseMatLocal * matGlobal.inverted()).to_quaternion()
(matGlobal * poseMatLocal * matGlobal.inverted()).to_quaternion()

toDeg((matGlobal.to_3x3() * poseMatLocal.to_3x3() * matGlobal.to_3x3().inverted()).to_euler())
toDeg((matGlobal.to_3x3() * poseMatGlobal.to_3x3() * matGlobal.to_3x3().inverted()).to_euler())
toDeg((matLocal.to_3x3() * poseMatLocal.to_3x3() * matLocal.to_3x3().inverted()).to_euler())
toDeg((matLocal.to_3x3() * poseMatGlobal.to_3x3() * matLocal.to_3x3().inverted()).to_euler())

toDeg((matGlobal.to_3x3() * poseMatGlobal.to_3x3() * matGlobal.to_3x3().inverted()).to_euler())
toDeg((matGlobal.to_3x3() * poseMatGlobal.to_3x3() * matGlobal.to_3x3().inverted()).to_euler())
toDeg((matGlobal.to_3x3() * poseMatGlobal.to_3x3() * matGlobal.to_3x3().inverted()).to_euler())
toDeg((matGlobal.to_3x3() * poseMatGlobal.to_3x3() * matGlobal.to_3x3().inverted()).to_euler())




poseMatGlobal = bpy.context.active_pose_bone.matrix_basis.copy() #LOCAL
matLocal = bpy.context.active_pose_bone.bone.matrix_local.copy() #LOCAL EditBoneRot

toDeg((matLocal.to_3x3() * poseMatGlobal.to_3x3() * matLocal.to_3x3().inverted()).to_euler())


#poseBone.matrix = matGlobal.to_4x4()
#poseBone.matrix = matLocal

rot = Euler((0,radians(50),0),'YXZ')

#>>> rot = Euler((0,radians(50),0),'YXZ')
#>>> bpy.context.active_pose_bone.matrix_basis = poseMatLocal.inverted() * rot.to_matrix().to_4x4() * poseMatLocal
#>>> bpy.context.active_pose_bone.rotation_quaternion = (matLocal.to_4x4().inverted() * rot.to_matrix().to_4x4() * matLocal.to_4x4()).decompose()[1]

print('-'*80)
print('pose local', toDeg(poseMatLocal.to_euler('YXZ')))
print('pose global', toDeg(poseMatGlobal.to_euler('YXZ')))

print('edit local', toDeg(matLocal.to_euler('YXZ')))
print('edit global', toDeg(matGlobal.to_euler('YXZ')))

xx = matLocal.inverted() * poseMatLocal
print(toDeg(xx.to_euler('YXZ')))

#poseBone.matrix = poseMatLocal # Posision actual de la pose LOCAL
#poseBone.matrix = poseMatGlobal # Posision actual de la pose
#poseBone.matrix = matGlobal.to_4x4() #posicion EJES
#poseBone.matrix = matLocal #posicion EDIT

#poseBone.matrix_basis = poseMatLocal
#poseBone.matrix_basis = poseMatGlobal
#poseBone.matrix_basis = matGlobal.to_4x4()
#poseBone.matrix_basis = matLocal


#print(matLocal.inverted().to_euler('YXZ'))

