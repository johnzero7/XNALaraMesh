# <pep8 compliant>

import io
import operator

from . import bin_ops
from . import read_bin_xps
from . import xps_const


def writeFilesString(string):
    byteString = bytearray()
    length1 = 0

    stringBin = bin_ops.writeString(string)
    length = len(stringBin)
    divQuot, divRem = divmod(length, xps_const.LIMIT)

    if (length >= xps_const.LIMIT):
        length1 += xps_const.LIMIT

    # First Lenght Byte
    length1 += divRem
    byteString.append(length1)

    if (divQuot):
        # Second Lenght Byte
        length2 = divQuot
        byteString.append(length2)
    byteString.extend(stringBin)
    return byteString


def writeVertexColor(co):
    r = bin_ops.writeByte(co[0])
    g = bin_ops.writeByte(co[1])
    b = bin_ops.writeByte(co[2])
    a = bin_ops.writeByte(co[3])
    vertexColor = bytearray()
    vertexColor.extend(r)
    vertexColor.extend(g)
    vertexColor.extend(b)
    vertexColor.extend(a)
    return vertexColor


def writeUvVert(co):
    x = bin_ops.writeSingle(co[0])  # X pos
    y = bin_ops.writeSingle(co[1])  # Y pos
    coords = bytearray()
    coords.extend(x)
    coords.extend(y)
    return coords


def writeXYZ(co):
    x = bin_ops.writeSingle(co[0])  # X pos
    y = bin_ops.writeSingle(co[1])  # Y pos
    z = bin_ops.writeSingle(co[2])  # Z pos
    coords = bytearray()
    coords.extend(x)
    coords.extend(y)
    coords.extend(z)
    return coords


def write4Float(co):
    x = bin_ops.writeSingle(co[0])  # X pos
    y = bin_ops.writeSingle(co[1])  # Y pos
    z = bin_ops.writeSingle(co[2])  # Z pos
    w = bin_ops.writeSingle(co[3])  # W pos
    coords = bytearray()
    coords.extend(x)
    coords.extend(y)
    coords.extend(z)
    coords.extend(w)
    return coords


def write4UInt16(co):
    r = bin_ops.writeInt16(co[0])
    g = bin_ops.writeInt16(co[1])
    b = bin_ops.writeInt16(co[2])
    a = bin_ops.writeInt16(co[3])
    vertexColor = bytearray()
    vertexColor.extend(r)
    vertexColor.extend(g)
    vertexColor.extend(b)
    vertexColor.extend(a)
    return vertexColor


def writeTriIdxs(co):
    face1 = bin_ops.writeUInt32(co[0])
    face2 = bin_ops.writeUInt32(co[1])
    face3 = bin_ops.writeUInt32(co[2])
    faceLoop = bytearray()
    faceLoop.extend(face1)
    faceLoop.extend(face2)
    faceLoop.extend(face3)
    return faceLoop


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


def writeHeader(xpsSettings, header):
    headerArray = bytearray()
    if header:
        # MagicNumber
        headerArray.extend(bin_ops.writeUInt32(header.magic_number))
        # XPS Model Version
        headerArray.extend(bin_ops.writeUInt16(header.version_mayor))
        headerArray.extend(bin_ops.writeUInt16(header.version_minor))
        # XNAaral Name
        headerArray.extend(writeFilesString(header.xna_aral))
        # Settings Len (unit32*4)
        headerArray.extend(bin_ops.writeUInt32(header.settingsLen))
        # MachineName
        headerArray.extend(writeFilesString(header.machine))
        # UserName
        headerArray.extend(writeFilesString(header.user))
        # File-->File
        headerArray.extend(writeFilesString(header.files))
        # settings
        headerArray.extend(header.settings)

    return headerArray


def writeBones(xpsSettings, bones):
    bonesArray = bytearray()
    if bones:
        bonesArray.extend(bin_ops.writeUInt32(len(bones)))

        for bone in bones:
            name = bone.name
            parentId = bone.parentId
            co = bone.co
            if parentId is None:
                parentId = -1
            bonesArray.extend(writeFilesString(name))
            bonesArray.extend(bin_ops.writeInt16(parentId))
            bonesArray.extend(writeXYZ(co))
    return bonesArray


def writeMeshes(xpsSettings, meshes):
    meshCount = len(meshes)
    meshesArray = bytearray(bin_ops.writeUInt32(meshCount))
    sortedMeshes = sorted(meshes, key=operator.attrgetter('name'))

    verMayor = xpsSettings.versionMayor
    verMinor = xpsSettings.versionMinor
    hasHeader = bin_ops.hasHeader(xpsSettings.format)

    hasTangent = bin_ops.hasTangentVersion(verMayor, verMinor, hasHeader)
    hasVariableWeights = bin_ops.hasVariableWeights(verMayor, verMinor, hasHeader)

    for mesh in sortedMeshes:
        # Name
        meshesArray.extend(writeFilesString(mesh.name))
        # uv Count
        meshesArray.extend(bin_ops.writeUInt32(mesh.uvCount))
        # Textures
        meshesArray.extend(bin_ops.writeUInt32(len(mesh.textures)))
        for texture in mesh.textures:
            meshesArray.extend(writeFilesString(texture.file))
            meshesArray.extend(bin_ops.writeUInt32(texture.uvLayer))

        # Vertices
        meshesArray.extend(bin_ops.writeUInt32(len(mesh.vertices)))
        for vertex in mesh.vertices:
            meshesArray.extend(writeXYZ(vertex.co))
            meshesArray.extend(writeXYZ(vertex.norm))
            meshesArray.extend(writeVertexColor(vertex.vColor))

            for uv in vertex.uv:
                meshesArray.extend(writeUvVert(uv))
            if hasTangent:
                meshesArray.extend(write4Float([1,0,0,0]))

            # Sort first the biggest weights
            boneWeights = sorted(
                vertex.boneWeights,
                key=lambda bw: bw.weight,
                reverse=True)

            if hasVariableWeights:
                weightCount = len(boneWeights)
                meshesArray.extend(bin_ops.writeUInt16(weightCount))
                [meshesArray.extend(bin_ops.writeUInt16(bw.id)) for bw in boneWeights]
                [meshesArray.extend(bin_ops.writeSingle(bw.weight)) for bw in boneWeights]
            else:
                meshesArray.extend(write4UInt16([bw.id for bw in boneWeights]))
                meshesArray.extend(write4Float([bw.weight for bw in boneWeights]))

        # Faces
        meshesArray.extend(bin_ops.writeUInt32(len(mesh.faces)))
        for face in mesh.faces:
            meshesArray.extend(writeTriIdxs(face))

    return meshesArray


def writeIoStream(filename, ioStream):
    with open(filename, "wb") as a_file:
        a_file.write(ioStream.read())


def writeXpsModel(xpsSettings, filename, xpsData):
    ioStream = io.BytesIO()
    print('Writing Header')
    ioStream.write(writeHeader(xpsSettings, xpsData.header))
    print('Writing Bones')
    ioStream.write(writeBones(xpsSettings, xpsData.bones))
    print('Writing Meshes')
    ioStream.write(writeMeshes(xpsSettings, xpsData.meshes))
    ioStream.seek(0)

    writeIoStream(filename, ioStream)


if __name__ == "__main__":
    readfilename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suitxxz\Generic_Item - XPS pose.mesh'
    writefilename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suitxxz\Generic_Item - BLENDER pose.mesh'

    # Simulate XPS Data
    # from . import mock_xps_data
    # xpsData = mock_xps_data.mockData()

    # import XPS File
    xpsData = read_bin_xps.readXpsModel(readfilename1)

    print('----WRITE START----')
    writeXpsModel(writefilename1, xpsData)
    print('----WRITE END----')
