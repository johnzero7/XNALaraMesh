# -*- coding: utf-8 -*-
# <pep8 compliant>

from getpass import getuser
from socket import gethostname

from . import bin_ops
from . import xps_const
from . import xps_types
import bpy


def mockData():
    xpsHeader = buildHeader()
    bones = buildBones()
    meshes = buildMeshes()
    xpsData = xps_types.XpsData(xpsHeader, bones, meshes)

    return xpsData


def fillPoseString(poseBytes):
    poseLenghtUnround = len(poseBytes)
    poseLenght = bin_ops.roundToMultiple(
        poseLenghtUnround, xps_const.ROUND_MULTIPLE)
    emptyFill = b'0' * (poseLenght - poseLenghtUnround)
    return poseBytes + emptyFill


def getPoseStringLength(poseString):
    return len(poseString)


def bonePoseCount(poseString):
    boneList = poseString.split('\n')
    return len(boneList) - 1


def buildHeader(poseString=''):
    invertUserName = getuser()[::-1]
    invertHostName = gethostname()[::-1]
    header = xps_types.XpsHeader()
    header.magic_number = xps_const.MAGIC_NUMBER
    header.version_mayor = xps_const.XPS_VERSION_MAYOR
    header.version_minor = xps_const.XPS_VERSION_MINOR
    header.xna_aral = xps_const.XNA_ARAL
    header.machine = invertHostName
    header.user = invertUserName
    header.files = '{}@{}'.format(invertUserName, bpy.data.filepath)
    # header.settings = bytes([0])*
    #     (xps_const.SETTINGS_LEN * xps_const.ROUND_MULTIPLE)

    boneCount = bonePoseCount(poseString)
    poseBytes = poseString.encode(xps_const.ENCODING_WRITE)
    default_pose = fillPoseString(poseBytes)
    poseLengthUnround = getPoseStringLength(poseString)

    var_1 = bin_ops.writeUInt32(180)  # Hash
    var_2 = bin_ops.writeUInt32(3)  # Items

    var_3 = bin_ops.writeUInt32(1)  # Type
    var_4 = bin_ops.writeUInt32(poseLengthUnround)  # Pose Lenght Unround
    var_5 = bin_ops.writeUInt32(boneCount)  # Pose Bone Counts
    # POSE DATA
    var_6 = bin_ops.writeUInt32(2)  # Type
    var_7 = bin_ops.writeUInt32(4)  # Count
    var_8 = bin_ops.writeUInt32(4)  # Info
    var_9 = bin_ops.writeUInt32(2)  # Count N1
    var_10 = bin_ops.writeUInt32(1)  # Count N2
    var_11 = bin_ops.writeUInt32(3)  # Count N3
    var_12 = bin_ops.writeUInt32(0)  # Count N4
    var_13 = bin_ops.writeUInt32(4)  # Type
    var_14 = bin_ops.writeUInt32(3)  # Count
    var_15 = bin_ops.writeUInt32(5)  # Info
    var_16 = bin_ops.writeUInt32(4)
    var_17 = bin_ops.writeUInt32(0)
    var_18 = bin_ops.writeUInt32(256)

    header_empty = b''
    header_empty += var_6
    header_empty += var_7
    header_empty += var_8
    header_empty += var_9
    header_empty += var_10
    header_empty += var_11
    header_empty += var_12
    header_empty += var_13
    header_empty += var_14
    header_empty += var_15
    header_empty += var_16
    header_empty += var_17
    header_empty += var_18

    header_unk = var_1 + var_2 + var_3
    header_pose = var_4 + var_5 + default_pose
    empty_count = ((xps_const.SETTINGS_LEN - len(header_empty)) // 4)
    header_empty += bin_ops.writeUInt32(0) * empty_count

    settings = header_unk + header_pose + header_empty
    header.settingsLen = len(settings) // 4
    header.settings = settings

    # logHeader(header)
    return header


def buildBones():
    bones = []

    id = 0
    name = 'bone1'
    co = [0, 0, 0]
    parentId = -1
    bone = xps_types.XpsBone(id, name, co, parentId)
    bones.append(bone)

    id = 1
    name = 'bone2'
    co = [0.5, 0.5, 0.5]
    parentId = 0
    bone = xps_types.XpsBone(id, name, co, parentId)
    bones.append(bone)
    return bones


def buildMeshes():
    meshes = []
    meshName = 'Mesh1'
    uvLayerCount = 1

    # Textures
    textures = []
    texId = 0
    textureFile = 'textutefile1.png'
    uvLayerId = 0
    xpsTexture = xps_types.XpsTexture(texId, textureFile, uvLayerId)
    textures.append(xpsTexture)

    texId = 1
    textureFile = 'textutefile2.png'
    uvLayerId = 0
    xpsTexture = xps_types.XpsTexture(texId, textureFile, uvLayerId)
    textures.append(xpsTexture)

    # Vertices
    vertex = []

    # Vertex1
    vertexId = 0
    coord = (1, 0, 0)
    normal = (0, 0, 1)
    vertexColor = (255, 255, 255, 0)
    uvs = []
    uvs.append((.2, .4))
    boneWeights = (
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0))
    xpsVertex = xps_types.XpsVertex(
        vertexId, coord, normal, vertexColor, uvs, boneWeights)

    # Vertex2
    vertexId = 1
    coord = (0, 1, 0)
    normal = (0, 1, 0)
    vertexColor = (255, 255, 255, 0)
    uvs = []
    uvs.append((.3, .5))
    boneWeights = (
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0))
    xpsVertex = xps_types.XpsVertex(
        vertexId, coord, normal, vertexColor, uvs, boneWeights)
    vertex.append(xpsVertex)

    # Vertex3
    vertexId = 2
    coord = (0, 0, 1)
    normal = (1, 0, 0)
    vertexColor = (255, 255, 255, 0)
    uvs = []
    uvs.append((.3, .9))
    boneWeights = (
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0),
        xps_types.BoneWeight(0, 0))
    xpsVertex = xps_types.XpsVertex(
        vertexId, coord, normal, vertexColor, uvs, boneWeights)
    vertex.append(xpsVertex)

    faces = []
    face = (0, 1, 2)
    faces.append(face)

    xpsMesh = xps_types.XpsMesh(
        meshName, textures, vertex, faces, uvLayerCount)
    meshes.append(xpsMesh)

    return meshes

if __name__ == "__main__":
    print('BUILD')
    xx = mockData()
    print('FINISH')
