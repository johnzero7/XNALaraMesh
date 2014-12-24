# -*- coding: utf-8 -*-

from XNALaraMesh import xps_const
from XNALaraMesh import xps_types
from XNALaraMesh import bin_ops
from XNALaraMesh import read_ascii_xps

import os
import io

def readFilesString(file):
    lengthByte2 = 0

    lengthByte1 = bin_ops.readByte(file)

    if (lengthByte1 >= xps_const.LIMIT):
        lengthByte2 = bin_ops.readByte(file)
    length = (lengthByte1 % xps_const.LIMIT) + (lengthByte2 * xps_const.LIMIT)

    string = bin_ops.readString(file, length)
    return string

def readVertexColor(file):
    r = bin_ops.readByte(file)
    g = bin_ops.readByte(file)
    b = bin_ops.readByte(file)
    a = bin_ops.readByte(file)
    vertexColor = [r, g, b, a]
    return vertexColor

def readUvVert(file):
    x = bin_ops.readSingle(file) # X pos
    y = bin_ops.readSingle(file) # Y pos
    coords = [x, y]
    return coords

def readXYZ(file):
    x = bin_ops.readSingle(file) # X pos
    y = bin_ops.readSingle(file) # Y pos
    z = bin_ops.readSingle(file) # Z pos
    coords = [x, y, z]
    return coords

def read4Float(file):
    x = bin_ops.readSingle(file)
    y = bin_ops.readSingle(file)
    z = bin_ops.readSingle(file)
    w = bin_ops.readSingle(file)
    coords = [x, y, z, w]
    return coords

def read4UInt16(file):
    r = bin_ops.readInt16(file)
    g = bin_ops.readInt16(file)
    b = bin_ops.readInt16(file)
    a = bin_ops.readInt16(file)
    vertexColor = [r, g, b, a]
    return vertexColor

def readTriIdxs(file):
    face1 = bin_ops.readUInt32(file)
    face2 = bin_ops.readUInt32(file)
    face3 = bin_ops.readUInt32(file)
    faceLoop = [face1, face2, face3]
    return faceLoop

def readHeader(file):
    header = None

    #Check for MAGIC_NUMBER
    number = bin_ops.readUInt32(file)
    file.seek(0)

    if (number == xps_const.MAGIC_NUMBER):
        print('Header Found')
        header = xps_types.XpsHeader()

        #MagicNumber
        magic_number = bin_ops.readUInt32(file)
        #XPS Version?
        xps_version = bin_ops.readUInt32(file)
        #XNAaral Name
        xna_aral = readFilesString(file)
        #Settings Length
        settingsLen = bin_ops.readUInt32(file)
        #MachineName
        machineName = readFilesString(file)
        #UserName
        userName = readFilesString(file)
        #File-->File
        filesString = readFilesString(file)
        #settings (20 bytes + posedata + bytes)
        unknownVar1 = bin_ops.readUInt32(file)
        unknownvar2 = bin_ops.readUInt32(file)
        unknownvar3 = bin_ops.readUInt32(file)
        poseLenghtUnround = bin_ops.readUInt32(file)
        poseBones = bin_ops.readUInt32(file)
        
        if poseBones:
            xpsPoseData = readDefaultPose(file, poseLenghtUnround, poseBones)
            header.pose = xpsPoseData

        #read Settings
        settings = file.read(xps_const.SETTINGS_LEN)

        header.magic_number = magic_number
        header.xps_version = xps_version
        header.xna_aral = xna_aral
        header.settingsLen = settingsLen
        header.machine = machineName
        header.user = userName
        header.files = filesString
        header.settings = settings

    #logHeader(header)
    return header

def logHeader(xpsHeader):
    print("MAGIX:",xpsHeader.magic_number)
    print('VER:',xpsHeader.xps_version)
    print('NAME:',xpsHeader.xna_aral)
    print('SETTINGS LEN:',xpsHeader.settingsLen)
    print('MACHINE:',xpsHeader.machine)
    print('USR:',xpsHeader.user)
    print('FILES:',xpsHeader.files)
    print('SETTING:',xpsHeader.settings)
    print('DEFAULT POSE:',xpsHeader.pose)

def readBones(file):
    bones = []
    #Bone Count
    boneCount = bin_ops.readUInt32(file)
    for boneId in range(boneCount):
        boneName = readFilesString(file)
        parentId = bin_ops.readInt16(file)
        coords = readXYZ(file)

        xpsBone = xps_types.XpsBone(boneId, boneName, coords, parentId)
        bones.append(xpsBone)
    return bones

def readMeshes(file, hasHeader):
    meshes = []
    meshCount = bin_ops.readUInt32(file)

    for meshId in range(meshCount):
        #Name
        meshName = readFilesString(file)
        #print('Mesh Name', meshName)
        #uv Count
        uvLayerCount = bin_ops.readUInt32(file)
        #Textures
        textures = []
        textureCount = bin_ops.readUInt32(file)
        for texId in range(textureCount):
            textureFile = os.path.basename(readFilesString(file))
            #print('Texture file', textureFile)
            uvLayerId = bin_ops.readUInt32(file)

            xpsTexture = xps_types.XpsTexture(texId, textureFile, uvLayerId)
            textures.append(xpsTexture)

        #Vertices
        vertex = []
        vertexCount = bin_ops.readUInt32(file)
        for vertexId in range(vertexCount):
            coord = readXYZ(file)
            normal = readXYZ(file)
            vertexColor = readVertexColor(file)

            uvs = []
            for uvLayerId in range(uvLayerCount):
                uvVert = readUvVert(file)
                uvs.append(uvVert)
                if not hasHeader:
                    tangent = read4Float(file)

            ###TODO Check if no bones
            boneIdx = read4UInt16(file)
            boneWeight = read4Float(file)

            xpsVertex = xps_types.XpsVertex(vertexId, coord, normal, vertexColor, uvs, boneIdx, boneWeight)
            vertex.append(xpsVertex)

        #Faces
        faces = []
        triCount = bin_ops.readUInt32(file)
        for i in range(triCount):
            triIdxs = readTriIdxs(file)
            faces.append(triIdxs)
        xpsMesh = xps_types.XpsMesh(meshName, textures, vertex, faces, uvLayerCount)
        meshes.append(xpsMesh)
    return meshes

def readPoseFile(file):
    return file.read()

def readIoStream(filename):
    with open(filename, "rb") as a_file:
        ioStream = io.BytesIO(a_file.read())
    return ioStream

def readXpsModel(filename):
    print('File:', filename)

    ioStream = readIoStream(filename)
    print('Reading Header')
    xpsHeader = readHeader(ioStream)
    hasHeader = bool(xpsHeader)
    print('Reading Bones')
    bones = readBones(ioStream)
    print('Read',len(bones),'Bones')
    print('Reading Meshes')
    meshes = readMeshes(ioStream, hasHeader)
    print('Read',len(meshes),'Meshes')

    xpsData = xps_types.XpsData(xpsHeader, bones, meshes)
    return xpsData

def readDefaultPose(file, poseLenghtUnround, poseBones):
    print('Import Pose')
    poseBytes = b''
    for i in range(0, poseBones):
        poseBytes += file.readline()

    poseLenght = bin_ops.roundToMultiple(poseLenghtUnround, xps_const.ROUND_MULTIPLE)
    emptyBytes = poseLenght - poseLenghtUnround
    file.read(emptyBytes)
    poseString = bin_ops.decodeBytes(poseBytes)
    bonesPose = read_ascii_xps.poseData(poseString)
    return bonesPose

if __name__ == "__main__":
    #readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item.mesh'
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item2.mesh'
    #readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item3.mesh'

    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\read.mesh.ascii'
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\write00.mesh'
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\Generic_Item_org.mesh'


    readfilename = r'G:\3DModeling\ExportTest\Cube\cube-pose.mesh'

    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING4\Street Fighter\Cammy Sexy and Tattooed\Generic_Item-pose.mesh'
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING4\Street Fighter\Cammy Sexy and Tattooed\Generic_Item-nono.mesh'
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING4\Street Fighter\Cammy Sexy and Tattooed\Generic_Item-pose2.mesh'
    #readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING4\Street Fighter\Cammy Sexy and Tattooed\Generic_Item-nono2.mesh'
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING2\Alisa\Alisa Erotic\Generic_Item.mesh'

    readfilename0 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - XPS.mesh'
    readfilename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - XPS pose.mesh'
    readfilename2 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - BLENDER.mesh'
    readfilename3 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - BLENDER pose.mesh'

    print('----READ START----')
    xpsData = readXpsModel(readfilename1)
    print('----READ END----')
