# -*- coding: utf-8 -*-

import copy
import math
import operator
import os
import re
import sys
import traceback

from XNALaraMesh import ascii_ops
from XNALaraMesh import import_xnalara_pose
from XNALaraMesh import read_ascii_xps
from XNALaraMesh import read_bin_xps
from XNALaraMesh import xps_material
from XNALaraMesh import xps_types
from XNALaraMesh.timing import timing
import bpy
from mathutils import *
import mathutils
# imported XPS directory
rootDir = ''
blenderBoneNames = None


class BlenderBoneNames:

    def __init__(self):
        self.bones = []


def newBoneName():
    global blenderBoneNames
    blenderBoneNames = BlenderBoneNames()
    return blenderBoneNames


def addBoneName(blenderBoneName):
    global blenderBoneNames
    blenderBoneNames.bones.append(blenderBoneName)


def getBoneName(originalIndex):
    return blenderBoneNames.bones[originalIndex]


def coordTransform(coords):
    x, y, z = coords
    z = -z
    return (x, z, y)


def faceTransform(face):
    return [face[0], face[2], face[1]]


def faceTransformList(faces):
    transformed = [faceTransform(face) for face in faces]
    return transformed


def uvTransform(uv):
    u = uv[0] - xpsSettings.uvDisplX
    v = xpsSettings.uvDisplY - uv[1]
    return [u, v]


def rangeFloatToByte(float):
    return int(float * 255) % 256


def rangeByteToFloat(byte):
    return float / 255


def uvTransformLayers(uvLayers):
    return [uvTransform(uv) for uv in uvLayers]


def getArmature():
    selected_obj = bpy.context.selected_objects
    armature_obj = next(
        (obj for obj in selected_obj if obj.type == 'ARMATURE'), None)
    return armature_obj


def makeImageFilepath(textureFilename):
    return os.path.join(rootDir, textureFilename)


def makeTexture(imageFilepath):
    image = loadImage(imageFilepath)
    # print("image:", str(image))
    # image.use_premultiply = True
    image.alpha_mode = 'PREMUL'

    imgTex = bpy.data.textures.new(imageFilepath, type='IMAGE')
    imgTex.name = image.name
    imgTex.image = image
    return imgTex


def newTextureSlot(materialData):
    textureSlot = materialData.texture_slots.add()
    textureSlot.texture_coords = "UV"
    # textureSlot.texture = imgTex
    textureSlot.use_map_alpha = True
    textureSlot.alpha_factor = 1.0
    return textureSlot


def makeMaterial(me_ob, meshInfo):
    meshFullName = meshInfo.name
    textureFilepaths = meshInfo.textures

    materialData = bpy.data.materials.new(meshFullName)
    materialData.use_transparent_shadows = True
    me_ob.materials.append(materialData)

    renderType = xps_material.makeRenderType(meshFullName)

    rGroup = xps_material.RenderGroup(renderType)

    for texIndex, textureInfo in enumerate(textureFilepaths):
        textureFilename = textureInfo.file
        textureUvLayer = textureInfo.uvLayer
        try:
            textureBasename = os.path.basename(textureFilename)

            # load image
            imageFilepath = makeImageFilepath(textureBasename)
            imgTex = makeTexture(imageFilepath)

            textureSlot = newTextureSlot(materialData)
            textureSlot.texture = imgTex
            textureSlot.use = False

            if (me_ob.uv_layers):
                textureSlot.uv_layer = me_ob.uv_layers[textureUvLayer].name

            xps_material.textureSlot(rGroup, texIndex, materialData)
            print("Texture: " + textureSlot.name)

        except Exception as inst:
            print("Error loading " + textureBasename)
            print(traceback.format_exc())

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)
            # If error loading texture, turn transparency off
            materialData.alpha = 1.0
            materialData.use_transparency = True


def getInputFilename(xpsSettingsAux):
    global xpsSettings
    xpsSettings = xpsSettingsAux

    blenderImportSetup()
    status = xpsImport()
    blenderImportFinalize()
    return status


def blenderImportSetup():
    # switch to object mode and deselect all
    objectMode()
    bpy.ops.object.select_all(action='DESELECT')


def blenderImportFinalize():
    # switch to object mode
    objectMode()


def objectMode():
    current_mode = bpy.context.mode
    if bpy.context.scene.objects.active and current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def loadXpsFile(filename):
    dirpath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    if ext.lower() in ('.mesh', '.xps'):
        xpsData = read_bin_xps.readXpsModel(filename)
    elif ext.lower() in('.ascii'):
        xpsData = read_ascii_xps.readXpsModel(filename)
    else:
        xpsData = None

    return xpsData


def makeMesh(meshFullName):
    mesh_da = bpy.data.meshes.new(meshFullName)
    mesh_ob = bpy.data.objects.new(mesh_da.name, mesh_da)
    print("Created Mesh: " + meshFullName)
    print("New Mesh = " + mesh_da.name)
    bpy.context.scene.objects.link(mesh_ob)
    # bpy.context.scene.update()
    # mesh_da.update()
    return mesh_ob


def setUvTexture(mesh_ob):
    if(mesh_ob.materials[0]):
        if(mesh_ob.materials[0].texture_slots[0]):
            currUvTexture = mesh_ob.materials[0].texture_slots[0].texture.image
            print("Seting UV " + currUvTexture.name)
            if mesh_ob.uv_textures.active:
                for uv_face in mesh_ob.uv_textures.active.data:
                    uv_face.image = currUvTexture


def loadImage(textureFilename):
    textureBasename = os.path.basename(textureFilename)
    fileRoot, fileExt = os.path.splitext(textureBasename)
    
    image = bpy.data.images.get(textureBasename)
    
    if image is None:
        print("Loading Texture: " + textureBasename)
        if (os.path.exists(textureFilename)):
            image = bpy.data.images.load(filepath=textureFilename)
            print("Texture load complete: " + textureBasename)
        else:
            print("Warning. Texture not found " + textureBasename)
            image = bpy.data.images.new(
                name=textureBasename, width=1024, height=1024, alpha=True,
                float_buffer=False)
            image.source = 'FILE'
            image.filepath = textureFilename
    return image


@timing
def xpsImport():
    global rootDir
    global xpsData

    print("------------------------------------------------------------")
    print("---------------EXECUTING XPS PYTHON IMPORTER----------------")
    print("------------------------------------------------------------")
    print("Importing file: ", xpsSettings.filename)

    rootDir, file = os.path.split(xpsSettings.filename)
    print("rootDir: " + rootDir)

    xpsData = loadXpsFile(xpsSettings.filename)
    if not xpsData:
        return '{NONE}'

    if not isModProtected(xpsData):
        # imports the armature
        armature_ob = importArmature(xpsSettings.autoIk)
        # imports all the meshes
        meshes_obs = importMeshesList(armature_ob)

        if armature_ob:
            hideUnusedBones([armature_ob])
            # set tail to Children Middle Point
            boneTailMiddleObject(armature_ob, xpsSettings.connectBones)

        if(xpsSettings.importDefaultPose and armature_ob):
            if(xpsData.header and xpsData.header.pose):
                import_xnalara_pose.setXpsPose(
                    armature_ob, xpsData.header.pose)
        return '{FINISHED}'
    else:
        print('This Model is Mod-Protected.Contact the original creator for '
              'an unprotected version')
        return '{PROTECTED}'


def isModProtected(xpsData):
    return ('p_' in [mesh.name[0:2].lower() for mesh in xpsData.meshes])


def setMinimumLenght(bone):
    default_length = 0.01
    if bone.length == 0:
        bone.tail = bone.head - Vector((0, .001, 0))
    if bone.length < default_length:
        bone.length = default_length


def boneTailMiddleObject(armature_ob, connectBones):
    bpy.context.scene.objects.active = armature_ob

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    editBones = armature_ob.data.edit_bones
    boneTailMiddle(editBones, connectBones)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def setBoneConnect(connectBones):
    currMode = bpy.context.mode
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    editBones = bpy.context.scene.objects.active.data.edit_bones
    connectEditBones(editBones, connectBones)
    bpy.ops.object.mode_set(mode=currMode, toggle=False)


def connectEditBones(editBones, connectBones):
    for bone in editBones:
        if bone.parent:
            if bone.head == bone.parent.tail:
                bone.use_connect = connectBones


def getAllArmaturesForMesh(mesh_ob):
    armatures = [modifier.object for modifier in mesh_ob.modifiers
                 if modifier.type == "ARMATURE"]
    return armatures


def hideBonesByName(armature_objs):
    '''Hide bones that do not affect any mesh'''
    for armature in armature_objs:
        for bone in armature.data.bones:
            if bone.name.lower().startswith('unused'):
                hideBone(bone)


def hideBonesByVertexGroup(armature_objs):
    '''Hide bones that do not affect any mesh'''
    for armature in armature_objs:
        objs = [obj for obj in bpy.context.scene.objects
                if obj.type == 'MESH' and obj.modifiers and [
                    modif for modif in obj.modifiers if modif and
                    modif.type == 'ARMATURE' and modif.object == armature]]

        # leafBones = [bone for bone in armature.data.bones
        #              if not bone.children]
        rootBones = [bone for bone in armature.data.bones if not bone.parent]

        # cycle objects and get all vertex groups
        vertexgroups = set(
            [vg.name for obj in objs if obj.type == 'MESH'
             for vg in obj.vertex_groups])

        for bone in rootBones:
            recurBones(bone, vertexgroups, '')


def recurBones(bone, vertexgroups, name):
    visibleChild = False
    for childBone in bone.children:
        aux = recurBones(childBone, vertexgroups, name + '  ')
        visibleChild = visibleChild or aux

    visibleChain = bone.name in vertexgroups or visibleChild
    if not visibleChain:
        hideBone(bone)
    return visibleChain


def hideBone(bone):
    bone.layers[1] = True
    bone.layers[0] = False


def showBone(bone):
    bone.layers[0] = True
    bone.layers[1] = False


def visibleBone(bone):
    return bone.layers[0]


def showAllBones(armature_objs):
    '''Move all bones to layer 0'''
    for armature in armature_objs:
        for bone in armature.data.bones:
            showBone(bone)


def hideBoneChain(bone):
    hideBone(bone)
    parentBone = bone.parent
    if parentBone:
        hideBoneChain(parentBone)


def showBoneChain(bone):
    showBone(bone)
    parentBone = bone.parent
    if parentBone:
        showBoneChain(parentBone)


def hideUnusedBones(armature_objs):
    hideBonesByVertexGroup(armature_objs)
    hideBonesByName(armature_objs)


def changeBoneName(boneName, suffix, replace):
    newName = re.sub(suffix, '*side*', boneName, 0, re.I)
    newName = re.sub(' +', ' ', newName, 0, re.I)
    newName = str.strip(newName)
    if boneName != newName:
        newName = newName + replace
    return newName


def renameBonesToBlender(armatures_obs):
    currActive = bpy.context.active_object
    for armature in armatures_obs:
        bpy.context.scene.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        for edit_bones in armature.data.edit_bones:
            oldName = edit_bones.name
            suffix = 'left'
            if re.search(suffix, oldName, re.I):
                edit_bones.name = changeBoneName(oldName, suffix, '.L')
            suffix = 'right'
            if re.search(suffix, oldName, re.I):
                edit_bones.name = changeBoneName(oldName, suffix, '.R')
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = currActive


def renameBonesToXps(armatures_obs):
    currActive = bpy.context.active_object
    for armature in armatures_obs:
        bpy.context.scene.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        newName = ''
        for edit_bones in armature.data.edit_bones:
            oldName = edit_bones.name
            suffix = '\.L'
            if re.search(suffix, oldName, re.I):
                newName = re.sub(suffix, '', oldName, 0, re.I)
                newName = re.sub(' +', ' ', newName, 0, re.I)
                newName = re.sub('\*side\*', 'left', newName, 0, re.I)
                edit_bones.name = newName
            suffix = '\.R'
            if re.search(suffix, oldName, re.I):
                newName = re.sub(suffix, '', oldName, 0, re.I)
                newName = re.sub(' +', ' ', newName, 0, re.I)
                newName = re.sub('\*side\*', 'right', newName, 0, re.I)
                edit_bones.name = newName
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = currActive


def importArmature(autoIk):
    bones = xpsData.bones
    armature_ob = None
    if bones:
        boneCount = len(xpsData.bones)
        print('Importing Armature', str(boneCount), 'bones')

        armature_da = bpy.data.armatures.new("Armature")
        armature_da.draw_type = 'STICK'
        armature_ob = bpy.data.objects.new("Armature", armature_da)
        armature_ob.show_x_ray = True

        bpy.context.scene.objects.link(armature_ob)

        bpy.context.scene.objects.active = armature_ob
        bpy.ops.object.mode_set(mode='EDIT')

        newBoneName()
        # create all Bones
        for bone in bones:
            editBone = armature_ob.data.edit_bones.new(bone.name)
            # Bone index change after parenting. This keeps original index
            addBoneName(editBone.name)

            transformedBone = coordTransform(bone.co)
            editBone.head = Vector(transformedBone)
            editBone.tail = Vector(editBone.head) + Vector((0, 0, -.1))
            setMinimumLenght(editBone)

        # set all bone parents
        for bone in bones:
            if (bone.parentId >= 0):
                editBone = armature_da.edit_bones[bone.id]
                editBone.parent = armature_da.edit_bones[bone.parentId]
        markSelected(armature_ob)
        bpy.ops.object.mode_set(mode='OBJECT')
        armature_ob.data.use_auto_ik = autoIk
    return armature_ob


def calcCenter(coords):
    sum = None
    for coord in coords:
        if sum is None:
            sum = coord.xyz
        else:
            sum += coord.xyz
    if sum:
        center = sum / len(coords)
    return center


def boneTailMiddle(editBones, connectBones):
    '''Move bone tail to children middle point'''
    for bone in editBones:
        if visibleBone(bone):
            childBones = [childBone for childBone in bone.children
                          if visibleBone(childBone)]
        else:
            childBones = [childBone for childBone in bone.children]

        if childBones:
            # Set tail to children middle
            bone.tail = calcCenter(
                [childBone.head for childBone in childBones])
        else:
            # if no child, set tail acording to parent
            if bone.parent is not None:
                if bone.head.xyz != bone.parent.tail.xyz:
                    # Tail to diference between bone and parent
                    delta = bone.head.xyz - bone.parent.tail.xyz
                else:
                    # Tail to same lenght/direction than parent
                    delta = bone.parent.tail.xyz - bone.parent.head.xyz
                bone.tail = bone.head.xyz + delta

    # Set minimum bone length
    for bone in editBones:
        setMinimumLenght(bone)

    # Connect Bones to parent
    connectEditBones(editBones, connectBones)


def markSelected(ob):
    ob.select = True


def makeUvs(mesh_ob, faces, uvData):
    # Create UVLayers
    for i in range(len(uvData[0])):
        mesh_ob.uv_textures.new(name="UV" + str(i + 1))

    # Assign UVCoords
    for layerIdx, uvLayer in enumerate(mesh_ob.uv_layers):
        for faceId, face in enumerate(faces):
            for vertId, faceVert in enumerate(face):
                loopdId = (faceId * 3) + vertId
                uvCoor = uvData[faceVert][layerIdx]
                uvLayer.data[loopdId].uv = Vector(uvCoor)


def createJoinedMeshes():
    meshPartRegex = re.compile('(!.*)*([\d]+nPart)*!')
    sortedMeshesList = sorted(xpsData.meshes, key=operator.attrgetter('name'))
    joinedMeshesNames = list(
        {meshPartRegex.sub('', mesh.name, 0) for mesh in sortedMeshesList})
    joinedMeshesNames.sort()
    newMeshes = []
    for joinedMeshName in joinedMeshesNames:
        # for each joinedMeshName generate a list of meshes to join
        meshesToJoin = [mesh for mesh in sortedMeshesList if meshPartRegex.sub(
            '', mesh.name, 0) == joinedMeshName]

        totalVertexCount = 0
        vertexCount = 0
        meshCount = 0

        meshName = None
        textures = None
        vertex = None
        faces = None
        uvLayerCount = None

        # new name for the unified mesh
        meshName = meshPartRegex.sub('', meshesToJoin[0].name, 0)
        # all the meshses share the same textures
        textures = meshesToJoin[0].textures
        # all the meshses share the uv layers count
        uvCount = meshesToJoin[0].uvCount
        # all the new joined mesh names
        vertex = []
        faces = []
        for mesh in meshesToJoin:
            vertexCount = 0
            meshCount = meshCount + 1

            if len(meshesToJoin) > 1 or meshesToJoin[0] not in sortedMeshesList:
                # unify vertex
                for vert in mesh.vertices:
                    vertexCount = vertexCount + 1
                    newVertice = xps_types.XpsVertex(
                        vert.id + totalVertexCount, vert.co, vert.norm, vert.vColor, vert.uv, vert.boneWeights)
                    vertex.append(newVertice)
                # unify faces
                for face in mesh.faces:
                    newFace = [face[0] + totalVertexCount, face[1] +
                               totalVertexCount, face[2] + totalVertexCount]
                    faces.append(newFace)
            else:
                vertex = mesh.vertices
                faces = mesh.faces
            totalVertexCount = totalVertexCount + vertexCount

        # Creates the nuw unified mesh
        xpsMesh = xps_types.XpsMesh(meshName, textures, vertex, faces, uvCount)
        newMeshes.append(xpsMesh)
    return newMeshes


def importMeshesList(armature_ob):
    if xpsSettings.joinMeshParts:
        newMeshes = createJoinedMeshes()
    else:
        newMeshes = xpsData.meshes
    importedMeshes = [importMesh(armature_ob, meshInfo)
                      for meshInfo in newMeshes]
    return [mesh for mesh in importedMeshes if mesh]


def generateVertexKey(vertex):
    if xpsSettings.joinMeshRips:
        key = str(vertex.co) + str(vertex.norm)
    else:
        key = str(vertex.id) + str(vertex.co) + str(vertex.norm)
    return key


def importMesh(armature_ob, meshInfo):
    boneCount = len(xpsData.bones)
    # Create Mesh
    meshFullName = meshInfo.name
    print()
    print("---*** Importing Mesh " + meshFullName + " ***---")

    # Load UV Layers Count
    uvLayerCount = meshInfo.uvCount
    print("UV Layer Count: " + str(uvLayerCount))

    # Load Textures Count
    textureCount = len(meshInfo.textures)
    print("Texture Count: " + str(textureCount))

    # Load Textures Filepaths and UvLayers
    textureFilepaths = meshInfo.textures

    mesh_ob = None
    if len(meshInfo.vertices) >= 3:
        vertexIdx = [0] * len(meshInfo.vertices)
        mapVertexKeys = {}
        vertexDict = []
        vertexData = []
        uvLayers = []
        for vertex in meshInfo.vertices:
            uvLayers.append(uvTransformLayers(vertex.uv))
            vertexKey = generateVertexKey(vertex)
            if vertexKey in mapVertexKeys:
                vertexID = mapVertexKeys[vertexKey]
            else:
                vertexID = len(vertexData)
                mapVertexKeys[vertexKey] = vertexID
                newVert = copy.deepcopy(vertex)
                newVert.id = vertexID
                vertexData.append(newVert)
            # old ID to new ID
            vertexDict.append(vertexID)

        facesData = []
        for face in meshInfo.faces:
            facesData.append(
                (vertexDict[face[0]], vertexDict[face[1]], vertexDict[face[2]]))

        # merge Vertices of same coord and normal?
        mergeByNormal = True
        if mergeByNormal:
            vertices = vertexData
            facesList = facesData
        else:
            vertices = meshInfo.vertices
            facesList = meshInfo.faces

        # Create Mesh
        mesh_ob = makeMesh(meshFullName)
        mesh_da = mesh_ob.data

        coords = []
        normals = []
        vertColors = []
        vrtxList = []
        nbVrtx = []

        for vertex in vertices:
            coords.append(coordTransform(vertex.co))
            normals.append(coordTransform(vertex.norm))
            vertColors.append(vertex.vColor)
            # uvLayers.append(uvTransformLayers(vertex.uv))

        # Create Faces
        faces = faceTransformList(facesList)
        mesh_da.from_pydata(coords, [], faces)
        mesh_da.polygons.foreach_set(
            "use_smooth", [True] * len(mesh_da.polygons))

        # Make UVLayers
        origFaces = faceTransformList(meshInfo.faces)
        makeUvs(mesh_da, origFaces, uvLayers)

        # Make Material
        makeMaterial(mesh_da, meshInfo)

        # Set UV Textures
        setUvTexture(mesh_da)

        if armature_ob:
            setArmatureModifier(armature_ob, mesh_ob)
            setParent(armature_ob, mesh_ob)

        makeVertexGroups(mesh_ob, vertices)

        # makeBoneGroups
        if armature_ob:
            makeBoneGroups(armature_ob, mesh_ob)

        # mesh_da.update()
        markSelected(mesh_ob)

        #import custom normals
        verts_nor = xpsSettings.importNormals
        use_edges = True
        unique_smooth_groups = True

        if verts_nor:
            mesh_da.create_normals_split()
            meshCorrected = mesh_da.validate(clean_customdata=False)  # *Very* important to not remove nors!
            mesh_da.update(calc_edges=use_edges)
            mesh_da.normals_split_custom_set_from_vertices(normals)
            mesh_da.use_auto_smooth = True
        else:
            meshCorrected = mesh_da.validate()
        
        print("Geometry Corrected:", meshCorrected)

    return mesh_ob


def setArmatureModifier(armature_ob, mesh_ob):
    mod = mesh_ob.modifiers.new(type="ARMATURE", name="Armature")
    mod.use_vertex_groups = True
    mod.object = armature_ob


def setParent(armature_ob, mesh_ob):
    mesh_ob.parent = armature_ob


def makeVertexGroups(mesh_ob, vertices):
    '''Make vertex groups and assign weights'''
    for vertex in vertices:
        for i in range(len(vertex.boneWeights)):
            boneIdx = vertex.boneWeights[i].id
            vertexWeight = vertex.boneWeights[i].weight
            if boneIdx > 0 and vertexWeight != 0:
                # blender limits vertexGroupNames to 63 chars
                armatures = getAllArmaturesForMesh(mesh_ob)
                for armature in armatures:
                    # use original index to get current bone name in blender
                    vertexGroupName = getBoneName(boneIdx)
                    bone = armature.data.bones[vertexGroupName]
                    vertGroup = mesh_ob.vertex_groups.get(vertexGroupName)
                    if not vertGroup:
                        vertGroup = mesh_ob.vertex_groups.new(vertexGroupName)
                    vertGroup.add([vertex.id], vertexWeight, 'REPLACE')


def makeBoneGroups(armature_ob, mesh_ob):
    import random
    C = bpy.context
    # Use current theme for selecte and active bone colors
    current_theme = C.user_preferences.themes.items()[0][0]
    theme = C.user_preferences.themes[current_theme]

    # random bone surface color by mesh
    bone_pose_surface_color = (
        random.random(), random.random(), random.random())
    bone_pose_color = theme.view_3d.bone_pose
    bone_pose_active_color = theme.view_3d.bone_pose_active

    # Store scene mode for later
    previous_mode = C.mode
    boneNames = mesh_ob.vertex_groups.keys()

    bpy.ops.object.mode_set(mode='POSE')
    boneGroup = getBoneGroup(mesh_ob.name)
    boneGroup.colors.normal = bone_pose_surface_color
    boneGroup.colors.select = bone_pose_color
    boneGroup.colors.active = bone_pose_active_color

    for boneName in boneNames:
        armature_ob.pose.bones[boneName].bone_group = boneGroup
    bpy.ops.object.mode_set(mode=previous_mode)


def getBoneGroup(name):
    bpy.ops.pose.group_add()
    bvhrig = bpy.context.scene.objects.active
    bvhgroup = bvhrig.pose.bone_groups.active
    bvhgroup.name = name
    bvhgroup.color_set = 'CUSTOM'
    return bvhgroup

if __name__ == "__main__":

    impDefPose = True
    joinMeshRips = True
    joinMesheParts = True
    uvDisplX = 0
    uvDisplY = 0
    connectBones = True
    autoIk = True

    readfilename = r'C:\XPS Tutorial\Yaiba MOMIJIII\momi3.mesh.mesh'

    xpsSettings = xps_types.XpsImportSettings(
        readfilename, uvDisplX, uvDisplY, impDefPose, joinMeshRips,
        joinMesheParts, connectBones, autoIk)
    getInputFilename(xpsSettings)
