# -*- coding: utf-8 -*-

from XNALaraMesh import xps_const
from XNALaraMesh import xps_types
from XNALaraMesh import ascii_ops

import bpy
import os
import io
import mathutils
from mathutils import *

def readUvVert(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    x = (ascii_ops.getFloat(values[0])) # X pos
    y = (ascii_ops.getFloat(values[1])) # Y pos
    coords = [x, y]
    return coords

def readXYZ(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    x = (ascii_ops.getFloat(values[0])) # X pos
    y = (ascii_ops.getFloat(values[1])) # Y pos
    z = (ascii_ops.getFloat(values[2])) # Z pos
    coords = [x, y, z]
    return coords

def fillArray(array, minLen, value):
    #Complete the array with selected value
    filled = array + [value]*(minLen - len(array))
    return filled

def read4Float(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    values = fillArray(values, 4, 0)
    x = (ascii_ops.getFloat(values[0]))
    y = (ascii_ops.getFloat(values[1]))
    z = (ascii_ops.getFloat(values[2]))
    w = (ascii_ops.getFloat(values[3]))
    coords = [x, y, z, w]
    return coords

def readBoneWeight(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    values = fillArray(values, 4, 0)
    weights = [ascii_ops.getFloat(val) for val in values]
    return weights

def readBoneId(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    values = fillArray(values, 4, 0)
    ids = [ascii_ops.getInt(val) for val in values]
    return ids

def read4Int(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    values = fillArray(values, 4, 0)
    r = ascii_ops.getInt(values[0])
    g = ascii_ops.getInt(values[1])
    b = ascii_ops.getInt(values[2])
    a = ascii_ops.getInt(values[3])
    vertexColor = [r, g, b, a]
    return vertexColor

def readTriIdxs(file):
    line = ascii_ops.readline(file)
    values = ascii_ops.splitValues(line)
    face1 = ascii_ops.getInt(values[0])
    face2 = ascii_ops.getInt(values[1])
    face3 = ascii_ops.getInt(values[2])
    faceLoop = [face1, face2, face3]
    return faceLoop

def readBones(file):
    bones = []
    #Bone Count
    boneCount = ascii_ops.readInt(file)
    for boneId in range(boneCount):
        boneName = ascii_ops.readString(file)
        parentId = ascii_ops.readInt(file)
        coords = readXYZ(file)

        xpsBone = xps_types.XpsBone(boneId, boneName, coords, parentId)
        bones.append(xpsBone)
    return bones

def readMeshes(file):
    meshes = []
    meshCount = ascii_ops.readInt(file)

    for meshId in range(meshCount):
        #Name
        meshName = ascii_ops.readString(file)
        if not meshName:
            meshName = 'xxx'
        #print('Mesh Name', meshName)
        #uv Count
        uvLayerCount = ascii_ops.readInt(file)
        #Textures
        textures = []
        textureCount = ascii_ops.readInt(file)
        for texId in range(textureCount):
            textureFile = os.path.basename(ascii_ops.readString(file))
            #print('Texture file', textureFile)
            uvLayerId = ascii_ops.readInt(file)

            xpsTexture = xps_types.XpsTexture(texId, textureFile, uvLayerId)
            textures.append(xpsTexture)

        #Vertices
        vertex = []
        vertexCount = ascii_ops.readInt(file)
        for vertexId in range(vertexCount):
            coord = readXYZ(file)
            normal = readXYZ(file)
            vertexColor = read4Int(file)

            uvs = []
            for uvLayerId in range(uvLayerCount):
                uvVert = readUvVert(file)
                uvs.append(uvVert)
                #if ????
                #tangent????
                #tangent = read4float(file)

            ###TODO Check if no bones
            
            boneIdx = readBoneId(file)
            boneWeight = readBoneWeight(file)

            boneWeights = []
            for idx in range(len(boneIdx)):
                boneWeights.append(xps_types.BoneWeight(boneIdx[idx], boneWeight[idx]))
                
            xpsVertex = xps_types.XpsVertex(vertexId, coord, normal, vertexColor, uvs, boneWeights)
            vertex.append(xpsVertex)

        #Faces
        faces = []
        triCount = ascii_ops.readInt(file)
        for i in range(triCount):
            triIdxs = readTriIdxs(file)
            faces.append(triIdxs)
        xpsMesh = xps_types.XpsMesh(meshName, textures, vertex, faces, uvLayerCount)
        meshes.append(xpsMesh)
    return meshes

def readPoseFile(file):
    return file.read()

def poseData(string):
    poseData = {}
    poseList = string.split('\n')
    for bonePose in poseList:
        if bonePose:
            pose = bonePose.split(':')
            
            boneName = pose[0]
            dataList = fillArray(pose[1].split(), 9, 1)
            rotDelta = Vector((ascii_ops.getFloat(dataList[0]), ascii_ops.getFloat(dataList[1]), ascii_ops.getFloat(dataList[2])))
            coordDelta = Vector((ascii_ops.getFloat(dataList[3]), ascii_ops.getFloat(dataList[4]), ascii_ops.getFloat(dataList[5])))
            scale = Vector((ascii_ops.getFloat(dataList[6]), ascii_ops.getFloat(dataList[7]), ascii_ops.getFloat(dataList[8])))
            
            bonePose = xps_types.XpsBonePose(boneName, coordDelta, rotDelta, scale)
            poseData[boneName] = bonePose
    return poseData

def readIoStream(filename):
    with open(filename, "r", encoding=xps_const.ENCODING_READ) as a_file:
        ioStream = io.StringIO(a_file.read())
    return ioStream

def readXpsModel(filename):
    ioStream = readIoStream(filename)
    #print('Reading Header')
    #xpsHeader = readHeader(ioStream)
    print('Reading Bones')
    bones = readBones(ioStream)
    print('Reading Meshes')
    meshes = readMeshes(ioStream)
    xpsModelData = xps_types.XpsData(bones=bones, meshes=meshes)
    return xpsModelData

def readXpsPose(filename):
    ioStream = readIoStream(filename)
    #print('Import Pose')
    poseString = readPoseFile(ioStream)
    bonesPose = poseData(poseString)
    return bonesPose

if __name__ == "__main__":
    #readModelfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item.mesh.ascii'
    readModelfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item2.mesh.ascii'
    #readModelfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item3.mesh.ascii'

    readModelfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item2.mesh.ascii'
    
    readModelfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\generic_item.mesh.ascii'
    readPosefilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Tekken\Tekken - Lili Bride\Lili 1.pose'

    print('----READ START----')
    xpsData = readXpsModel(readModelfilename)
    xpsData = readXpsPose(readPosefilename)
    print('----READ END----')
