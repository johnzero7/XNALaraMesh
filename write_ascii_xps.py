# <pep8 compliant>

import io
import operator

from . import read_ascii_xps
from . import xps_const
from mathutils import Vector


def writeBones(bones):
    bonesString = io.StringIO()
    if bones:
        bonesString.write('{:d} # bones\n'.format(len(bones)))

        for bone in bones:
            name = bone.name
            parentId = bone.parentId
            co = bone.co
            if parentId is None:
                parentId = -1
            bonesString.write('{}\n'.format(name))
            bonesString.write('{:d} # parent index\n'.format(parentId))
            bonesString.write('{:.7G} {:.7G} {:.7G}\n'.format(*co))
    bonesString.seek(0)
    return bonesString


def writeMeshes(meshes):
    meshesString = io.StringIO()
    meshesString.write('{:d} # meshes\n'.format(len(meshes)))
    sortedMeshes = sorted(meshes, key=operator.attrgetter('name'))

    for mesh in sortedMeshes:
        # Name
        meshesString.write(mesh.name + '\n')
        # uv Count
        meshesString.write('{:d} # uv layers\n'.format(mesh.uvCount))
        # Textures
        meshesString.write('{:d} # textures\n'.format(len(mesh.textures)))
        for texture in mesh.textures:
            meshesString.write(texture.file + '\n')
            meshesString.write(
                '{:d} # uv layer index\n'.format(texture.uvLayer))

        # Vertices
        meshesString.write('{:d} # vertices\n'.format(len(mesh.vertices)))
        for vertex in mesh.vertices:
            meshesString.write(
                '{:.7G} {:.7G} {:.7G} # Coords\n'.format(*vertex.co))
            meshesString.write('{:.7G} {:.7G} {:.7G}\n'.format(*vertex.norm))
            meshesString.write('{:d} {:d} {:d} {:d}\n'.format(*vertex.vColor))

            for uv in vertex.uv:
                meshesString.write('{:.7G} {:.7G}\n'.format(*uv))
                # if ????
                # tangent????
                # meshesString.write(write4float(xxx))

            length = len(vertex.boneWeights)
            idFormatString = ' '.join(['{:d}', ] * length)
            weightFormatString = ' '.join(['{:.7G}', ] * length)

            # Sort first the biggest weights
            boneWeights = sorted(
                vertex.boneWeights,
                key=lambda bw: bw.weight,
                reverse=True)

            meshesString.write(
                (idFormatString + '\n').format(*[bw.id for bw in boneWeights]))
            meshesString.write(
                (weightFormatString + '\n').format(*[bw.weight for bw in boneWeights]))

        # Faces
        meshesString.write('{:d} # faces\n'.format(len(mesh.faces)))
        for face in mesh.faces:
            meshesString.write('{:d} {:d} {:d}\n'.format(*face))

    meshesString.seek(0)
    return meshesString


def writePose(xpsData):
    poseString = io.StringIO()
    sortedPose = sorted(xpsData.items(), key=operator.itemgetter(0))

    for boneData in sortedPose:
        xpsBoneData = boneData[1]
        boneName = xpsBoneData.boneName
        rotDelta = roundRot(xpsBoneData.rotDelta)
        coordDelta = roundTrans(xpsBoneData.coordDelta)
        scale = roundScale(xpsBoneData.scale)

        x1 = '{}: '.format(boneName)
        x2 = '{:G} {:G} {:G} '.format(*rotDelta)
        x3 = '{:G} {:G} {:G} '.format(*coordDelta)
        x4 = '{:G} {:G} {:G} '.format(*scale)

        poseString.write(x1)
        poseString.write(x2)
        poseString.write(x3)
        poseString.write(x4)
        poseString.write('\n')

    poseString.seek(0)
    return poseString


def writeXpsPose(filename, xpsData):
    ioStream = io.StringIO()
    print('Export Pose')
    ioStream.write(writePose(xpsData).read())
    ioStream.seek(0)
    writeIoStream(filename, ioStream)


def roundRot(vector):
    x = round(vector.x, 1) + 0
    y = round(vector.y, 1) + 0
    z = round(vector.z, 1) + 0
    return Vector((x, y, z))


def roundTrans(vector):
    x = round(vector.x, 4) + 0
    y = round(vector.y, 4) + 0
    z = round(vector.z, 4) + 0
    return Vector((x, y, z))


def roundScale(vector):
    x = round(vector.x, 3) + 0
    y = round(vector.y, 3) + 0
    z = round(vector.z, 3) + 0
    return Vector((x, y, z))


def writeIoStream(filename, ioStream):
    with open(filename, "w", encoding=xps_const.ENCODING_WRITE) as a_file:
        a_file.write(ioStream.read())


def writeBoneDict(filename, boneDictList):
    ioStream = io.StringIO()
    ioStream.write(boneDictList)
    ioStream.seek(0)
    writeIoStream(filename, ioStream)


def writeXpsModel(filename, xpsData):
    ioStream = io.StringIO()
    # print('Writing Header')
    # ioStream.write(writeHeader(xpsData.header))
    print('Writing Bones')
    ioStream.write(writeBones(xpsData.bones).read())
    print('Writing Meshes')
    ioStream.write(writeMeshes(xpsData.meshes).read())
    ioStream.seek(0)
    writeIoStream(filename, ioStream)


if __name__ == "__main__":
    readfilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item2.mesh.ascii'
    writefilename = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING\Alice Returns - Mods\Alice 001 Fetish Cat\generic_item3.mesh.ascii'

    # Simulate XPS Data
    # from . import mock_xps_data
    # xpsData = mock_xps_data.mockData()

    # import XPS File
    xpsData = read_ascii_xps.readXpsModel(readfilename)

    print('----WRITE START----')
    writeXpsModel(writefilename, xpsData)
    print('----WRITE END----')
