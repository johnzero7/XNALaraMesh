import os
from . import import_xnalara_pose
from . import export_xnalara_pose
from . import mock_xps_data
from . import write_ascii_xps
from . import write_bin_xps
from . import bin_ops
from . import xps_material
from . import xps_types
from . import node_shader_utils
from .timing import timing

import bpy
from mathutils import Vector
from collections import Counter

# imported XPS directory
rootDir = ''


def coordTransform(coords):
    x, y, z = coords
    y = -y
    return (x, z, y)


def faceTransform(face):
    return [face[0], face[2], face[1]]


def uvTransform(uv):
    u = uv[0] + xpsSettings.uvDisplX
    v = 1 - xpsSettings.uvDisplY - uv[1]
    return [u, v]


def rangeFloatToByte(float):
    return int(float * 255) % 256


def rangeByteToFloat(byte):
    return byte / 255


def uvTransformLayers(uvLayers):
    return list(map(uvTransform, uvLayers))


def getArmature(selected_obj):
    armature_obj = next((obj for obj in selected_obj
                         if obj.type == 'ARMATURE'), None)
    return armature_obj


def fillArray(array, minLen, value):
    # Complete the array with selected value
    filled = array + [value] * (minLen - len(array))
    return filled


def getOutputFilename(xpsSettingsAux):
    global xpsSettings
    xpsSettings = xpsSettingsAux

    blenderExportSetup()
    xpsExport()
    blenderExportFinalize()


def blenderExportSetup():
    # switch to object mode and deselect all
    objectMode()


def blenderExportFinalize():
    pass


def objectMode():
    current_mode = bpy.context.mode
    if bpy.context.view_layer.objects.active and current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def saveXpsFile(filename, xpsData):
    dirpath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    if ext.lower() in ('.mesh', '.xps'):
        write_bin_xps.writeXpsModel(xpsSettings, filename, xpsData)
    elif ext.lower() in('.ascii'):
        write_ascii_xps.writeXpsModel(xpsSettings, filename, xpsData)


@timing
def xpsExport():
    global rootDir
    global xpsData

    print("------------------------------------------------------------")
    print("---------------EXECUTING XPS PYTHON EXPORTER----------------")
    print("------------------------------------------------------------")
    print("Exporting file: ", xpsSettings.filename)

    if xpsSettings.exportOnlySelected:
        exportObjects = bpy.context.selected_objects
    else:
        exportObjects = bpy.context.visible_objects

    selectedArmature, selectedMeshes = exportSelected(exportObjects)

    xpsBones = exportArmature(selectedArmature)
    xpsMeshes = exportMeshes(selectedArmature, selectedMeshes)

    poseString = ''
    if(xpsSettings.expDefPose):
        xpsPoseData = export_xnalara_pose.xpsPoseData(selectedArmature)
        poseString = write_ascii_xps.writePose(xpsPoseData).read()

    header = None
    hasHeader = bin_ops.hasHeader(xpsSettings.format)
    if hasHeader:
        header = mock_xps_data.buildHeader(poseString)
        header.version_mayor = xpsSettings.versionMayor
        header.version_minor = xpsSettings.versionMinor
    xpsData = xps_types.XpsData(header=header, bones=xpsBones,
                                meshes=xpsMeshes)

    saveXpsFile(xpsSettings.filename, xpsData)


def exportSelected(objects):
    meshes = []
    armatures = []
    armature = None
    for object in objects:
        if object.type == 'ARMATURE':
            armatures.append(object)
        elif object.type == 'MESH':
            meshes.append(object)
        armature = object.find_armature() or armature
    # armature = getArmature(objects)
    return armature, meshes


def exportArmature(armature):
    xpsBones = []
    if armature:
        bones = armature.data.bones
        print('Exporting Armature', len(bones), 'Bones')
        # activebones = [bone for bone in bones if bone.layers[0]]
        activebones = bones
        for bone in activebones:
            objectMatrix = armature.matrix_local
            id = bones.find(bone.name)
            name = bone.name
            co = coordTransform(objectMatrix @ bone.head_local.xyz)
            parentId = None
            if bone.parent:
                parentId = bones.find(bone.parent.name)
            xpsBone = xps_types.XpsBone(id, name, co, parentId)
            xpsBones.append(xpsBone)
    if not xpsBones:
        xpsBone = xps_types.XpsBone(0, 'root', (0, 0, 0), -1)
        xpsBones.append(xpsBone)

    return xpsBones


def exportMeshes(selectedArmature, selectedMeshes):
    xpsMeshes = []
    for mesh in selectedMeshes:
        print('Exporting Mesh:', mesh.name)
        meshName = makeNamesFromMesh(mesh)
        # meshName = makeNamesFromMaterials(mesh)
        meshTextures = getXpsMatTextures(mesh)
        meshVerts, meshFaces = getXpsVertices(selectedArmature, mesh)
        meshUvCount = len(mesh.data.uv_layers)

        materialsCount = len(mesh.data.materials)
        if (materialsCount > 0):
            for idx in range(materialsCount):
                xpsMesh = xps_types.XpsMesh(meshName[idx], meshTextures[idx],
                                            meshVerts[idx], meshFaces[idx],
                                            meshUvCount)
                xpsMeshes.append(xpsMesh)
        else:
            dummyTexture = [xps_types.XpsTexture(0, 'dummy.png', 0)]
            xpsMesh = xps_types.XpsMesh(meshName[0], dummyTexture,
                                        meshVerts[0], meshFaces[0],
                                        meshUvCount)
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
    separatedMeshNames.append(xps_material.makeRenderTypeName(renderType))

    materialsCount = len(mesh.data.materials)
    # separate mesh by materials
    for mat_idx in range(1, materialsCount):
        partName = '{0}.material{1:02d}'.format(meshName, mat_idx)
        renderType.meshName = partName
        fullName = xps_material.makeRenderTypeName(renderType)
        separatedMeshNames.append(fullName)
    return separatedMeshNames


def addTexture(tex_dic, texture_type, texture):
    if texture is not None:
        tex_dic[texture_type] = texture


def getTextureFilename(texture):
    textureFile = None
    if texture and texture.image is not None:
        texFilePath = texture.image.filepath
        absFilePath = bpy.path.abspath(texFilePath)
        texturePath, textureFile = os.path.split(absFilePath)
    return textureFile


def makeXpsTexture(mesh, material):
    active_uv = mesh.data.uv_layers.active
    active_uv_index = mesh.data.uv_layers.active_index
    xpsShaderWrapper = node_shader_utils.XPSShaderWrapper(material)

    tex_dic = {}
    texture = getTextureFilename(xpsShaderWrapper.diffuse_texture)
    addTexture(tex_dic, xps_material.TextureType.DIFFUSE, texture)
    texture = getTextureFilename(xpsShaderWrapper.lightmap_texture)
    addTexture(tex_dic, xps_material.TextureType.LIGHT, texture)
    texture = getTextureFilename(xpsShaderWrapper.normalmap_texture)
    addTexture(tex_dic, xps_material.TextureType.BUMP, texture)
    texture = getTextureFilename(xpsShaderWrapper.normal_mask_texture)
    addTexture(tex_dic, xps_material.TextureType.MASK, texture)
    texture = getTextureFilename(xpsShaderWrapper.microbump1_texture)
    addTexture(tex_dic, xps_material.TextureType.BUMP1, texture)
    texture = getTextureFilename(xpsShaderWrapper.microbump2_texture)
    addTexture(tex_dic, xps_material.TextureType.BUMP2, texture)
    texture = getTextureFilename(xpsShaderWrapper.specular_texture)
    addTexture(tex_dic, xps_material.TextureType.SPECULAR, texture)
    texture = getTextureFilename(xpsShaderWrapper.environment_texture)
    addTexture(tex_dic, xps_material.TextureType.ENVIRONMENT, texture)
    texture = getTextureFilename(xpsShaderWrapper.emission_texture)
    addTexture(tex_dic, xps_material.TextureType.EMISSION, texture)

    renderType = xps_material.makeRenderType(mesh.name)
    renderGroup = xps_material.RenderGroup(renderType)
    rgTextures = renderGroup.rgTexType

    texutre_list = []
    for tex_type in rgTextures:
        texture = tex_dic.get(tex_type, 'missing.png')
        texutre_list.append(texture)

    xpsTextures = []
    for id, textute in enumerate(texutre_list):
        xpsTexture = xps_types.XpsTexture(id, textute, 0)
        xpsTextures.append(xpsTexture)

    return xpsTextures


def getTextures(mesh, material):
    textures = []
    xpsTextures = makeXpsTexture(mesh, material)
    return xpsTextures


def getXpsMatTextures(mesh):
    xpsMatTextures = []
    for material_slot in mesh.material_slots:
        material = material_slot.material
        xpsTextures = getTextures(mesh, material)
        xpsMatTextures.append(xpsTextures)
    return xpsMatTextures


def generateVertexKey(vertex, uvCoord, seamSideId):
    # Generate a unique key for vertex using coords,normal,
    # first UV and side of seam
    key = '{}{}{}{}'.format(vertex.co, vertex.normal, uvCoord, seamSideId)
    return key


def getXpsVertices(selectedArmature, mesh):
    mapMatVertexKeys = []  # remap vertex index
    xpsMatVertices = []  # Vertices separated by material
    xpsMatFaces = []  # Faces separated by material
    # xpsVertices = []  # list of vertices for a single material
    # xpsFaces = []  # list of faces for a single material

    exportVertColors = xpsSettings.vColors
    armature = mesh.find_armature()
    objectMatrix = mesh.matrix_world
    rotQuaternion = mesh.matrix_world.to_quaternion()

    verts_nor = xpsSettings.exportNormals

    # Calculates tesselated faces and normal split to make them available for export
    mesh.data.calc_normals_split()
    mesh.data.calc_loop_triangles()
    mesh.data.update(calc_edges=True)
    mesh.data.calc_loop_triangles()

    matCount = len(mesh.data.materials)
    if (matCount > 0):
        for idx in range(matCount):
            xpsMatVertices.append([])  # Vertices separated by material
            xpsMatFaces.append([])  # Faces separated by material
            mapMatVertexKeys.append({})
    else:
        xpsMatVertices.append([])  # Vertices separated by material
        xpsMatFaces.append([])  # Faces separated by material
        mapMatVertexKeys.append({})

    meshVerts = mesh.data.vertices
    meshEdges = mesh.data.edges
    # tessface accelerator
    hasSeams = any(edge.use_seam for edge in meshEdges)
    tessFaces = mesh.data.loop_triangles[:]
    # tessFaces = mesh.data.tessfaces
    tessface_uv_tex = mesh.data.uv_layers
    tessface_vert_color = mesh.data.vertex_colors
    meshEdgeKeys = mesh.data.edge_keys

    vertEdges = [[] for x in range(len(meshVerts))]
    tessEdgeFaces = {}

    preserveSeams = xpsSettings.preserveSeams
    if (preserveSeams and hasSeams):
        # Count edges for faces
        tessEdgeCount = Counter(tessEdgeKey for tessFace in tessFaces for tessEdgeKey in tessFace.edge_keys)

        # create dictionary. faces for each edge
        for tessface in tessFaces:
            for tessEdgeKey in tessface.edge_keys:
                if tessEdgeFaces.get(tessEdgeKey) is None:
                    tessEdgeFaces[tessEdgeKey] = []
                tessEdgeFaces[tessEdgeKey].append(tessface.index)

        # use Dict to speedup search
        edgeKeyIndex = {val: index for index, val in enumerate(meshEdgeKeys)}

        # create dictionary. Edges connected to each Vert
        for key in meshEdgeKeys:
            meshEdge = meshEdges[edgeKeyIndex[key]]
            vert1, vert2 = key
            vertEdges[vert1].append(meshEdge)
            vertEdges[vert2].append(meshEdge)

    faceEdges = []
    faceSeams = []

    for face in tessFaces:
        # faceIdx = face.index
        material_index = face.material_index
        xpsVertices = xpsMatVertices[material_index]
        xpsFaces = xpsMatFaces[material_index]
        mapVertexKeys = mapMatVertexKeys[material_index]
        faceVerts = []
        seamSideId = ''
        faceVertIndices = face.vertices[:]
        faceUvIndices = face.loops[:]

        for vertEnum, vertIndex in enumerate(faceVertIndices):
            vertex = meshVerts[vertIndex]

            if (preserveSeams and hasSeams):
                connectedFaces = set()
                faceEdges = vertEdges[vertIndex]
                faceSeams = [edge for edge in faceEdges if edge.use_seam]

                if (len(faceSeams) >= 1):
                    vertIsBorder = any(tessEdgeCount[edge.index] != 2 for edge in faceEdges)
                    if (len(faceSeams) > 1) or (len(faceSeams) == 1 and vertIsBorder):

                        oldFacesList = set()
                        connectedFaces = set([face])
                        while oldFacesList != connectedFaces:

                            oldFacesList = connectedFaces

                            allEdgeKeys = set(connEdgeKey for connface in connectedFaces for connEdgeKey in connface.edge_keys)
                            connEdgesKeys = [edge.key for edge in faceEdges]
                            connEdgesNotSeamsKeys = [seam.key for seam in faceSeams]

                            connectedEdges = allEdgeKeys.intersection(connEdgesKeys).difference(connEdgesNotSeamsKeys)
                            connectedFaces = set(tessFaces[connFace] for connEdge in connectedEdges for connFace in tessEdgeFaces[connEdge])

                            connectedFaces.add(face)

                faceIndices = [face.index for face in connectedFaces]
                seamSideId = '|'.join(str(faceIdx) for faceIdx in sorted(faceIndices))

            uvs = getUvs(tessface_uv_tex, faceUvIndices[vertEnum])
            vertexKey = generateVertexKey(vertex, uvs, seamSideId)

            if vertexKey in mapVertexKeys:
                vertexID = mapVertexKeys[vertexKey]
            else:
                vCoord = coordTransform(objectMatrix @ vertex.co)
                if verts_nor:
                    normal = Vector(face.split_normals[vertEnum])
                else:
                    normal = vertex.normal
                norm = coordTransform(rotQuaternion @ normal)
                vColor = getVertexColor(exportVertColors, tessface_vert_color, faceUvIndices[vertEnum])
                boneId, boneWeight = getBoneWeights(mesh, vertex, armature)

                boneWeights = []
                for idx in range(len(boneId)):
                    boneWeights.append(xps_types.BoneWeight(boneId[idx],
                                                            boneWeight[idx]))
                vertexID = len(xpsVertices)
                mapVertexKeys[vertexKey] = vertexID
                xpsVertex = xps_types.XpsVertex(vertexID, vCoord, norm, vColor, uvs,
                                                boneWeights)
                xpsVertices.append(xpsVertex)
            faceVerts.append(vertexID)

        meshFaces = getXpsFace(faceVerts)
        xpsFaces.extend(meshFaces)

    return xpsMatVertices, xpsMatFaces


def getUvs(tessface_uv_tex, uvIndex):
    uvs = []
    for tessface_uv_layer in tessface_uv_tex:
        uvCoord = tessface_uv_layer.data[uvIndex].uv
        uvCoord = uvTransform(uvCoord)
        uvs.append(uvCoord)
    return uvs


def getVertexColor(exportVertColors, tessface_vert_color, vColorIndex):
    vColor = None
    if exportVertColors and tessface_vert_color:
        vColor = tessface_vert_color[0].data[vColorIndex].color[:]
    else:
        vColor = [1, 1, 1, 1]

    vColor = list(map(rangeFloatToByte, vColor))
    return vColor


def getBoneWeights(mesh, vertice, armature):
    boneId = []
    boneWeight = []
    if armature:
        for vertGroup in vertice.groups:
            # Vertex Group
            groupIdx = vertGroup.group
            boneName = mesh.vertex_groups[groupIdx].name
            boneIdx = armature.data.bones.find(boneName)
            weight = vertGroup.weight
            if boneIdx < 0:
                boneIdx = 0
                weight = 0
            boneId.append(boneIdx)
            boneWeight.append(weight)
    boneId = fillArray(boneId, 4, 0)
    boneWeight = fillArray(boneWeight, 4, 0)
    return boneId, boneWeight


def getXpsFace(faceVerts):
    xpsFaces = []

    if len(faceVerts) == 3:
        xpsFaces.append(faceTransform(faceVerts))
    elif len(faceVerts) == 4:
        v1, v2, v3, v4 = faceVerts
        xpsFaces.append(faceTransform((v1, v2, v3)))
        xpsFaces.append(faceTransform((v3, v4, v1)))

    return xpsFaces


def boneDictGenerate(filepath, armatureObj):
    boneNames = sorted([import_xnalara_pose.renameBoneToXps(name) for name in armatureObj.data.bones.keys()])
    boneDictList = '\n'.join(';'.join((name,) * 2) for name in boneNames)
    write_ascii_xps.writeBoneDict(filepath, boneDictList)


if __name__ == "__main__":
    uvDisplX = 0
    uvDisplY = 0
    exportOnlySelected = True
    exportPose = False
    modProtected = False
    filename1 = (r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB '
                 r'DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by '
                 r'DamianHandy\Generic_Item - BLENDER pose.mesh')

    filename = r'C:\XPS Tutorial\Yaiba MOMIJIII\momi.mesh.ascii'

    xpsSettings = xps_types.XpsImportSettings(filename, uvDisplX, uvDisplY,
                                              exportOnlySelected, exportPose,
                                              modProtected)

    getOutputFilename(xpsSettings)
