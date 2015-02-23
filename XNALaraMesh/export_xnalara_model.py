# -*- coding: utf-8 -*-

from XNALaraMesh import write_ascii_xps
from XNALaraMesh import write_bin_xps
from XNALaraMesh import xps_types
from XNALaraMesh import mock_xps_data
from XNALaraMesh import export_xnalara_pose
from XNALaraMesh import xps_material

import bpy
import timeit
import time
#import math
import mathutils

import os


from mathutils import *

#imported XPS directory
rootDir = ''
def coordTransform(coords):
    x, y, z = coords
    y = -y
    return (x, z, y)

def faceTransform(face):
    return [face[0],face[2],face[1]]

def faceTransformList(faces):
    transformed = [faceTransform(face) for face in faces]
    return transformed

def uvTransform(uv):
    u = uv[0] - uvDisplX
    v = uvDisplY - uv[1]
    return [u, v]

def rangeFloatToByte(float):
    return int(float * 255)%256

def rangeByteToFloat(byte):
    return float/255

def uvTransformLayers(uvLayers):
    return [uvTransform(uv) for uv in uvLayers]

def getArmature():
    selected_obj = bpy.context.selected_objects
    armature_obj = next((obj for obj in selected_obj if obj.type == 'ARMATURE'), None)
    return armature_obj

def fillArray(array, minLen, value):
    #Complete the array with selected value
    filled = array + [value]*(minLen - len(array))
    return filled

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def getOutputFilename(filename, uvX, uvY, impSelected, exportPose, modProtected):
    global uvDisplX
    global uvDisplY
    global importSelected
    global expDefPose
    uvDisplX = uvX
    uvDisplY = uvY
    importSelected = impSelected
    expDefPose = exportPose

    blenderExportSetup()
    xpsExport(filename, modProtected)
    blenderExportFinalize()

def blenderExportSetup():
    # switch to object mode and deselect all
    objectMode()

def blenderExportFinalize():
    pass

def objectMode():
    current_mode = bpy.context.mode
    if bpy.context.scene.objects.active and current_mode!='OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def saveXpsFile(filename, xpsData):
    dirpath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    if ext in ('.mesh', '.xps'):
        write_bin_xps.writeXpsModel(filename, xpsData)
    elif ext in('.ascii'):
        write_ascii_xps.writeXpsModel(filename, xpsData)

@timing
def xpsExport(filename, modProtected):
    global rootDir
    global xpsData
    global importSelected

    print ("------------------------------------------------------------")
    print ("---------------EXECUTING XPS PYTHON EXPORTER----------------")
    print ("------------------------------------------------------------")
    print ("Exporting file: ", filename)

    if importSelected:
        exportObjects = bpy.context.selected_objects
    else:
        exportObjects = bpy.context.scene.objects

    selectedArmature, selectedMeshes = exportSelected(exportObjects)

    xpsBones = exportArmature(selectedArmature)
    xpsMeshes = exportMeshes(selectedArmature, selectedMeshes, modProtected)

    poseString = ''
    if(expDefPose):
        xpsPoseData = export_xnalara_pose.xpsPoseData(selectedArmature)
        poseString = write_ascii_xps.writePose(xpsPoseData).read()

    header = mock_xps_data.buildHeader(poseString)
    xpsData = xps_types.XpsData(header=header, bones=xpsBones, meshes=xpsMeshes)

    saveXpsFile(filename, xpsData)

def exportSelected(objects):
    meshes = []
    armatures = []
    for object in objects:
        if object.type == 'ARMATURE':
            armatures.append(object)
        elif object.type == 'MESH':
            meshes.append(object)
    armature = getArmature()
    return armature, meshes

def exportArmature(armature):
    xpsBones = []
    if armature:
        bones = armature.data.bones
        print('Exporting Armature', len(bones), 'Bones')
        #activebones = [bone for bone in bones if bone.layers[0]]
        activebones = bones
        for bone in activebones:
            objectMatrix = armature.matrix_local
            id = bones.find(bone.name)
            name = bone.name
            co = coordTransform(objectMatrix * bone.head_local.xyz)
            parentId = None
            if bone.parent:
                parentId = bones.find(bone.parent.name)
            xpsBone = xps_types.XpsBone(id, name, co, parentId)
            xpsBones.append(xpsBone)
    if not xpsBones:
        xpsBone = xps_types.XpsBone(0, 'root', (0,0,0), -1)
        xpsBones.append(xpsBone)
       
    return xpsBones

def exportMeshes(selectedArmature, selectedMeshes, modProtected):
    xpsMeshes = []
    if modProtected:
        xpsMesh = xps_types.XpsMesh('p_dummyobject_0_0_0', [], [], [], 0)
        xpsMeshes.append(xpsMesh)
    for mesh in selectedMeshes:
        print('Exporting Mesh:', mesh.name)
        meshName = makeNamesFromMesh(mesh)
        #meshName = makeNamesFromMaterials(mesh)
        meshTextures = getXpsMatTextures(mesh)
        meshVertices, meshFaces = getXpsVertices(selectedArmature, mesh)
        meshUvCount = len(mesh.data.uv_layers)

        materialsCount = len(mesh.data.materials)
        for idx in range(materialsCount):
            xpsMesh = xps_types.XpsMesh(meshName[idx], meshTextures[idx], meshVertices[idx], meshFaces[idx], meshUvCount)
            xpsMeshes.append(xpsMesh)

    return xpsMeshes

def makeNamesFromMaterials(mesh):
    separatedMeshNames = []
    materials = mesh.data.materials
    for material in materials:
        separatedMeshNames.append(material.name)
    return separatedMeshNames

def makeNamesFromMesh(mesh):
    meshFullName = mesh.name
    renderType = xps_material.makeRenderType(meshFullName)
    meshName = renderType.meshName
    
    separatedMeshNames = []
    separatedMeshNames.append(meshFullName)

    materialsCount = len(mesh.data.materials)
    for mat_idx in range(1, materialsCount):
        partName = meshName + ".part." + "{0:03d}".format(mat_idx)
        renderType.meshName = partName
        fullName = xps_material.makeRenderTypeName(renderType)
        separatedMeshNames.append(fullName)
    return separatedMeshNames

def getTextures(mesh, material):
    textures = []
    for textureSlot in material.texture_slots:
        if textureSlot and textureSlot.texture.type == 'IMAGE':
            xpsTexture = makeXpsTexture(mesh, material, textureSlot)
            textures.append(xpsTexture)
    return textures

def getXpsMatTextures(mesh):
    xpsMatTextures = []
    for material_slot in mesh.material_slots:
        material = material_slot.material
        xpsTextures = getTextures(mesh, material)
        xpsMatTextures.append(xpsTextures)
    return xpsMatTextures

def makeXpsTexture(mesh, material, textureSlot):
    texFilePath = textureSlot.texture.image.filepath
    absFilePath = bpy.path.abspath(texFilePath)
    #texFilePath = bpy.path.relpath(texFilePath)
    texturePath, textureFile = os.path.split(absFilePath)
    uvLayerName = textureSlot.uv_layer
    uvLayerIdx = mesh.data.uv_layers.find(uvLayerName)
    if uvLayerIdx == -1:
        uv_active_render = next((uv_texture for uv_texture in mesh.data.uv_textures if uv_texture.active_render == True))
        uvLayerIdx = mesh.data.uv_layers.find(uv_active_render.name)

    id = material.texture_slots.find(textureSlot.name)

    xpsTexture = xps_types.XpsTexture(id, textureFile, uvLayerIdx)
    return xpsTexture

def generateVertexKey(vertex, texCoords):
    key = str(vertex.co) + str(vertex.normal)
    for texCoord in texCoords:
        key += str(texCoord)
    return key

def getXpsVertices(selectedArmature, mesh):
    mapMatVertexKeys = [] #remap vertex index 
    xpsMatVertices = [] #Vertices separated by material
    xpsMatFaces = [] #Faces separated by material
    #xpsVertices = [] #list of vertices for a single material
    #xpsFaces = [] #list of faces for a single material

    uvIndexs = makeSimpleUvVert(mesh)
    vColors = makeSimpleVertColor(mesh)
    armature = getMeshArmature(selectedArmature, mesh)
    objectMatrix = mesh.matrix_world
    rotQuaternion = mesh.matrix_world.to_quaternion()

    mesh.data.update(calc_edges=True,calc_tessface=True)


    vertices = mesh.data.vertices
    matCount = len(mesh.data.materials)
    for idx in range(matCount):
        xpsMatVertices.append([]) #Vertices separated by material
        xpsMatFaces.append([]) #Faces separated by material
        mapMatVertexKeys.append({})

    for faceIdx, face in enumerate(mesh.data.tessfaces):
        material_index = face.material_index
        xpsVertices = xpsMatVertices[material_index]
        xpsFaces = xpsMatFaces[material_index]
        mapVertexKeys = mapMatVertexKeys[material_index]
        faceVerts = []
        for vertNum, vertIndex in enumerate(face.vertices):
            vertex = vertices[vertIndex]
            co = coordTransform(objectMatrix * vertex.co)
            norm = coordTransform(rotQuaternion * vertex.normal)
            vColor = getVertexColor()
            uv = getUvs(mesh, faceIdx, vertNum)
            boneId = getBonesId(mesh, vertex, armature)
            boneWeight = getBonesWeight(vertex)
            
            boneWeights=[]
            for idx in range(len(boneId)):
                boneWeights.append(xps_types.BoneWeight(boneId[idx], boneWeight[idx]))
                
            vertexKey = generateVertexKey(vertex, uv)
 
            if vertexKey in mapVertexKeys:
                vertexID = mapVertexKeys[vertexKey]
            else:
                vertexID = len(xpsVertices)
                mapVertexKeys[vertexKey] = vertexID
                xpsVertex = xps_types.XpsVertex(vertexID, co, norm, vColor, uv, boneWeights)
                xpsVertices.append(xpsVertex)
            faceVerts.append(vertexID)
        
        meshFaces = getXpsFace(faceVerts)
        xpsFaces.extend(meshFaces)

    return xpsMatVertices, xpsMatFaces

def makeSimpleUvVert(mesh):
    simpleUvIndex = [None] * len(mesh.data.vertices)
    for uvVert in mesh.data.loops:
        simpleUvIndex[uvVert.vertex_index] = uvVert.index
    return simpleUvIndex

def makeSimpleVertColor(mesh):
    simpleVertColors = [(255,255,255,0)] * len(mesh.data.vertices)
    vColors = None
    if mesh.data.vertex_colors:
        vColors = mesh.data.vertex_colors[0]
    if vColors:
        for uvVert in mesh.data.loops:
            color = vColors.data[uvVert.index].color
            r = rangeFloatToByte(color.r)
            g = rangeFloatToByte(color.g)
            b = rangeFloatToByte(color.b)
            a = 0
            simpleVertColors[uvVert.vertex_index] = (r, g, b, a)
    return simpleVertColors

def getModifierArmatures(mesh):
    return [modif.object for modif in mesh.modifiers if modif.type=="ARMATURE"]

def getMeshArmature(selectedArmature, mesh):
    armatures = getModifierArmatures(mesh)
    armature = None
    if selectedArmature in armatures:
        armature = selectedArmature
    return armature

def getUvs(mesh, faceIdx, vertNum):
    uvs = []
    for tessface_uv_layer in mesh.data.tessface_uv_textures:
        uvCoord = tessface_uv_layer.data[faceIdx].uv[vertNum]
        uvCoord = uvTransform(uvCoord)
        uvs.append(uvCoord)
    return uvs

def getVertexColor():
    return (255,255,255,0)

def getBonesId(mesh, vertice, armature):
    boneId = []
    if armature:
        for vertGroup in vertice.groups:
            #Vertex Group
            groupIdx = vertGroup.group
            boneName = mesh.vertex_groups[groupIdx].name
            boneIdx = armature.data.bones.find(boneName)
            boneId.append(boneIdx)
    boneId = fillArray(boneId, 4, 0)
    return boneId

def getBonesWeight(vertice):
    boneWeight = []
    for vertGroup in vertice.groups:
        boneWeight.append(vertGroup.weight)
    boneWeight = fillArray(boneWeight, 4, 0)
    return boneWeight

def getXpsFace(faceVerts):
    xpsFaces = []

    if len(faceVerts) == 3:
        xpsFaces.append(faceTransform(faceVerts))
    else:
        v1, v2, v3, v4 = faceVerts
        xpsFaces.append(faceTransform((v1, v2, v3)))
        xpsFaces.append(faceTransform((v1, v3, v4)))

    return xpsFaces

if __name__ == "__main__":
    impSelected = True
    exportPose = False
    modProtected = False
    #filename0 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - BLENDER.mesh'
    filename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - BLENDER pose.mesh'

    filename = r'C:\XPS Tutorial\Yaiba MOMIJIII\momi.mesh.ascii'

    getOutputFilename(filename, 0, 1, impSelected, exportPose, modProtected)




