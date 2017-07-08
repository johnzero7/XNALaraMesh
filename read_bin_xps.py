# -*- coding: utf-8 -*-
# <pep8 compliant>

import io
import ntpath

from . import bin_ops
from . import read_ascii_xps
from . import xps_const
from . import xps_types
import bpy


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
    x = bin_ops.readSingle(file)  # X pos
    y = bin_ops.readSingle(file)  # Y pos
    coords = [x, y]
    return coords


def readXYZ(file):
    x = bin_ops.readSingle(file)  # X pos
    y = bin_ops.readSingle(file)  # Y pos
    z = bin_ops.readSingle(file)  # Z pos
    coords = [x, y, z]
    return coords


def read4Float(file):
    x = bin_ops.readSingle(file)
    y = bin_ops.readSingle(file)
    z = bin_ops.readSingle(file)
    w = bin_ops.readSingle(file)
    coords = [x, y, z, w]
    return coords


def read4Int16(file):
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


def hasTangentHeader(xpsHeader):
    return (xpsHeader.version_mayor <= 1 and xpsHeader.version_minor <= 12)


def readHeader(file):
    header = xps_types.XpsHeader()

    # MagicNumber
    magic_number = bin_ops.readUInt32(file)
    # XPS Version
    version_mayor = bin_ops.readUInt16(file)
    version_minor = bin_ops.readUInt16(file)
    # XNAaral Name
    xna_aral = readFilesString(file)
    # Settings Length
    settingsLen = bin_ops.readUInt32(file)
    # MachineName
    machineName = readFilesString(file)
    # UserName
    userName = readFilesString(file)
    # File-->File
    filesString = readFilesString(file)
    xpsPoseData = None

    # print('*'*80)
    if (version_mayor <= 1 and version_minor <= 12):
        # print('OLD Format')
        settingsStream = io.BytesIO(file.read(settingsLen * 4))
    else:
        # print('NEW Format')
        valuesRead = 0
        hash = bin_ops.readUInt32(file)
        valuesRead += 1 * 4
        items = bin_ops.readUInt32(file)
        valuesRead += 1 * 4
        # print('hash', hash)
        # print('items', items)
        for i in range(items):
            # print('valuesRead', valuesRead)
            optType = bin_ops.readUInt32(file)
            valuesRead += 1 * 4
            optcount = bin_ops.readUInt32(file)
            valuesRead += 1 * 4
            optInfo = bin_ops.readUInt32(file)
            valuesRead += 1 * 4

            # print('------')
            # print('count',i)
            # print('optType',optType)
            # print('optcount',optcount)
            # print('optInfo',optInfo)

            if (optType == 255):
                # print('Read None')
                readNone(file, optcount)
                valuesRead += optcount * 2
            elif (optType == 2):
                # print('Read Flags')
                readFlags(file, optcount)
                valuesRead += optcount * 2 * 4
            elif (optType == 1):
                # print('Read Pose')
                xpsPoseData = readDefaultPose(file, optcount, optInfo)
                readCount = bin_ops.roundToMultiple(
                    optcount, xps_const.ROUND_MULTIPLE)
                valuesRead += readCount
            else:
                # print('Read Waste')
                loopStart = valuesRead // 4
                loopFinish = settingsLen
                # print (loopStart, loopFinish)
                for j in range(loopStart, loopFinish):
                    # print('waste',j - loopStart)
                    waste = bin_ops.readUInt32(file)

    header.magic_number = magic_number
    header.version_mayor = version_mayor
    header.version_minor = version_minor
    header.xna_aral = xna_aral
    header.settingsLen = settingsLen
    header.machine = machineName
    header.user = userName
    header.files = filesString
    header.pose = xpsPoseData
    return header


def findHeader(file):
    header = None

    # Check for MAGIC_NUMBER
    number = bin_ops.readUInt32(file)
    file.seek(0)

    if (number == xps_const.MAGIC_NUMBER):
        print('Header Found')
        header = readHeader(file)

    # logHeader(header)
    return header


def readNone(file, optcount):
    for i in range(optcount):
        waste = bin_ops.readUInt32(file)


def readFlags(file, optcount):
    for i in range(optcount * 2):
        waste = bin_ops.readUInt32(file)


def logHeader(xpsHeader):
    print("MAGIX:", xpsHeader.magic_number)
    print('VER MAYOR:', xpsHeader.version_mayor)
    print('VER MINOR:', xpsHeader.version_minor)
    print('NAME:', xpsHeader.xna_aral)
    print('SETTINGS LEN:', xpsHeader.settingsLen)
    print('MACHINE:', xpsHeader.machine)
    print('USR:', xpsHeader.user)
    print('FILES:', xpsHeader.files)
    print('SETTING:', xpsHeader.settings)
    print('DEFAULT POSE:', xpsHeader.pose)


def readBones(file):
    bones = []
    # Bone Count
    boneCount = bin_ops.readUInt32(file)
    for boneId in range(boneCount):
        boneName = readFilesString(file)
        parentId = bin_ops.readInt16(file)
        coords = readXYZ(file)

        xpsBone = xps_types.XpsBone(boneId, boneName, coords, parentId)
        bones.append(xpsBone)
    return bones


def readMeshes(file, xpsHeader, hasBones):
    meshes = []
    meshCount = bin_ops.readUInt32(file)
    hasHeader = bool(xpsHeader)
    hasTangent = False
    if hasHeader:
        hasTangent = hasTangentHeader(xpsHeader)

    for meshId in range(meshCount):
        # Name
        meshName = readFilesString(file)
        if not meshName:
            meshName = 'unnamed'
        # print('Mesh Name:', meshName)
        # uv Count
        uvLayerCount = bin_ops.readUInt32(file)
        # Textures
        textures = []
        textureCount = bin_ops.readUInt32(file)
        for texId in range(textureCount):
            textureFile = ntpath.basename(readFilesString(file))
            # print('Texture file', textureFile)
            uvLayerId = bin_ops.readUInt32(file)

            xpsTexture = xps_types.XpsTexture(texId, textureFile, uvLayerId)
            textures.append(xpsTexture)

        # Vertices
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
                if not hasHeader or hasTangent:
                    tangent = read4Float(file)

            boneWeights = []
            if hasBones:
                # if cero bones dont have weights to read
                boneIdx = read4Int16(file)
                boneWeight = read4Float(file)

                for idx in range(len(boneIdx)):
                    boneWeights.append(
                        xps_types.BoneWeight(boneIdx[idx], boneWeight[idx]))
            xpsVertex = xps_types.XpsVertex(
                vertexId, coord, normal, vertexColor, uvs, boneWeights)
            vertex.append(xpsVertex)

        # Faces
        faces = []
        triCount = bin_ops.readUInt32(file)
        for i in range(triCount):
            triIdxs = readTriIdxs(file)
            faces.append(triIdxs)
        xpsMesh = xps_types.XpsMesh(
            meshName, textures, vertex, faces, uvLayerCount)
        meshes.append(xpsMesh)
    return meshes


def readIoStream(filename):
    with open(filename, "rb") as a_file:
        ioStream = io.BytesIO(a_file.read())
    return ioStream


def readXpsModel(filename):
    print('File:', filename)

    ioStream = readIoStream(filename)
    print('Reading Header')
    xpsHeader = findHeader(ioStream)
    print('Reading Bones')
    bones = readBones(ioStream)
    hasBones = bool(bones)
    print('Read', len(bones), 'Bones')
    print('Reading Meshes')
    meshes = readMeshes(ioStream, xpsHeader, hasBones)
    print('Read', len(meshes), 'Meshes')

    xpsData = xps_types.XpsData(xpsHeader, bones, meshes)
    return xpsData


def readDefaultPose(file, poseLenghtUnround, poseBones):
    # print('Import Pose')
    poseBytes = b''
    if poseLenghtUnround:
        for i in range(0, poseBones):
            poseBytes += file.readline()

    poseLenght = bin_ops.roundToMultiple(
        poseLenghtUnround, xps_const.ROUND_MULTIPLE)
    emptyBytes = poseLenght - poseLenghtUnround
    file.read(emptyBytes)
    poseString = bin_ops.decodeBytes(poseBytes)
    bonesPose = read_ascii_xps.poseData(poseString)
    return bonesPose

if __name__ == "__main__":
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\Young Samus\Generic_Item.mesh'

    print('----READ START----')
    xpsData = readXpsModel(readfilename)
    print('----READ END----')
