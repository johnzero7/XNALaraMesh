# -*- coding: utf-8 -*-

from XNALaraMesh import read_ascii_xps
from XNALaraMesh import read_bin_xps
from XNALaraMesh import xps_types
from XNALaraMesh import import_xnalara_pose

import timeit
import time
import bpy
import mathutils
from mathutils import *

import os

#imported XPS directory
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

def makeImageFilepath(textureFilename):
    return os.path.join(rootDir, textureFilename)

def makeMaterial(me_ob, meshInfo):
    meshFullName = meshInfo.name
    textureFilepaths = meshInfo.textures

    matdata = bpy.data.materials.new(meshFullName)
    me_ob.materials.append(matdata)

    mat=meshFullName.split("_")
    maxLen=8
    #Complete the array with None
    mat = mat + [None]*(maxLen - len(mat))

    renderGroup = mat[0]
    meshName = mat[1]
    val1 = mat[2]
    val2 = mat[3]
    val3 = mat[4]
    val4 = mat[5]
    val5 = mat[6]
    val6 = mat[7]

    val1 = 0.0
    val2 = 0.0
    val3 = 0.0

    matdata.specular_intensity = 0.0
    matdata.alpha = 0.0
    matdata.use_transparency = True
    matdata.use_transparent_shadows = True
    matdata.use_face_texture = True
    texCounter = 0

    for texIndex, textureInfo in enumerate(textureFilepaths):
        textureFilename = textureInfo.file
        textureUvLayer = textureInfo.uvLayer
        try:
            ###TODO implement XPS rendergroup logic
            print("--")
            textureBasename = os.path.basename(textureFilename)

            #load image
            imageFilepath = makeImageFilepath(textureBasename)
            image = loadImage(imageFilepath)

            image.alpha_mode = 'PREMUL'
            #image.use_premultiply = True
            # print("image: " + str(image))
            imgTex = bpy.data.textures.new(imageFilepath, type='IMAGE')
            imgTex.name = image.name
            imgTex.image = image
            mtex = matdata.texture_slots.add()
            mtex.texture_coords = "UV"
            mtex.texture = imgTex
            mtex.use_map_alpha = True
            mtex.alpha_factor = 1.0

            if (me_ob.uv_layers):
                mtex.uv_layer = me_ob.uv_layers[textureUvLayer].name

            if (texIndex == 0):
                 mtex.use = True

            elif (mtex.name.lower().endswith("_n") or mtex.name.lower().find("_n.") != -1
                    or mtex.name.lower().endswith("_nm") or mtex.name.lower().find("_nm.") != -1
                    or mtex.name.lower().endswith("_norm") or mtex.name.lower().find("_norm.") != -1
                    or mtex.name.lower().find("bump") != -1 ):
                # we done have ourselves a normal map
                print("normal map")
                mtex.use = True
                mtex.use_map_color_diffuse = False
                mtex.normal_factor = 1.0
                mtex.normal_map_space = 'TANGENT'
                mtex.use_map_normal = True
                mtex.use_map_alpha = False
                imgTex.use_normal_map = True
                imgTex.image.use_alpha = False
            elif (mtex.name.lower().endswith("_s") or mtex.name.lower().find("_s.") != -1
                    or mtex.name.lower().endswith("_spec") or mtex.name.lower().find("_spec.") != -1):
                print("specular map")
                mtex.use = True
                mtex.use_map_color_diffuse = False
                mtex.use_map_alpha = False
                mtex.specular_factor = .2
                mtex.use_map_specular = True
                mtex.use_map_alpha = False
            else:
                mtex.use = False
                print("Not used")

            print("Texture: " + mtex.name)

        except Exception as inst:
            print("Error loading " + textureBasename)
            print (traceback.format_exc())

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            print (type(inst))  # the exception instance
            print (inst.args)   # arguments stored in .args
            print (inst)
            # If error loading texture, turn transparency off
            matdata.alpha = 1.0
            matdata.use_transparency = True

        texCounter = texCounter + 1;

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def getInputFilename(filename, removeUnusedBones, combineMeshes, uvX, uvY, importPose):
    global uvDisplX
    global uvDisplY
    global impDefPose
    uvDisplX = uvX
    uvDisplY = uvY
    impDefPose = importPose

    blenderImportSetup()
    xpsImport(filename, removeUnusedBones, combineMeshes)
    blenderImportFinalize()

def blenderImportSetup():
    # switch to object mode and deselect all
    objectMode()
    bpy.ops.object.select_all(action='DESELECT')

def blenderImportFinalize():
    # switch to object mode
    objectMode()

def objectMode():
    current_mode = bpy.context.mode
    if bpy.context.scene.objects.active and current_mode!='OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def loadXpsFile(filename):
    dirpath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    if ext in ('.mesh', '.xps'):
        xpsData = read_bin_xps.readXpsModel(filename)
    elif ext in('.ascii'):
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
    #bpy.context.scene.update()
    #mesh_da.update()
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

    print("Loading Texture: " + textureBasename)
    if (os.path.exists(textureFilename)):
        image = bpy.data.images.load(filepath=textureFilename)
        print("Texture load complete: " + textureBasename)
    else:
        print("Warning. Texture not found " + textureBasename)
        image = bpy.data.images.new(name=textureBasename, width=1024, height=1024, alpha=True, float_buffer=False)
        image.source='FILE'
        image.filepath=textureFilename
    return image

@timing
def xpsImport(filename, removeUnusedBones, combineMeshes):
    global rootDir
    global xpsData

    print ("------------------------------------------------------------")
    print ("---------------EXECUTING XPS PYTHON IMPORTER----------------")
    print ("------------------------------------------------------------")
    print ("Importing file: ", filename)

    rootDir, file = os.path.split(filename)
    print ("rootDir: " + rootDir)

    xpsData = loadXpsFile(filename)

    armature_ob = importArmature()
    meshes_obs = importMeshesList(armature_ob)

    hideUnusedBones(meshes_obs)
    #set tail to Children Middle Point

    boneTailMiddleObject(armature_ob)
    
    if(impDefPose):
        if(xpsData.header and xpsData.header.pose):
            import_xnalara_pose.setXpsPose(armature_ob, xpsData.header.pose)

def setMinumunLenght(bone):
        default_length = 0.02
        if bone.length == 0:
            bone.tail = bone.head - Vector((0, default_length, 0))
        if bone.length < default_length:
            bone.length = default_length

def boneTailMiddleObject(armature_ob):
    bpy.context.scene.objects.active = armature_ob

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    boneTailMiddle(armature_ob.data.edit_bones)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def getAllArmaturesForMesh(mesh_ob):
    armatures = [modifier.object for modifier in mesh_ob.modifiers if modifier.object.type == "ARMATURE"]
    return armatures

def hideAllBones(meshes_obs):
    #Move all bones to layer 2
    for mesh_ob in meshes_obs:
        armatures = getAllArmaturesForMesh(mesh_ob)
        for armature in set(armatures):
            for bone in armature.data.bones:
                bone.layers[1] = True
                bone.layers[0] = False

def moveUsedVertexGroupBones(armature_ob, meshes_obs):
    #Move used bones to layer 1
    for mesh_ob in meshes_obs:
        armatures = [modifier.object for modifier in mesh_ob.modifiers if modifier.object.type == "ARMATURE"]
        for armature in set(armatures):
            for vertexGroup in mesh_ob.vertex_groups:
                armature.data.bones[vertexGroup.name].layers[0] = True
                armature.data.bones[vertexGroup.name].layers[1] = False

def moveUsedBoneChain(meshes_obs):
    #Move used bonechain to layer 1
    for mesh_ob in meshes_obs:
        armatures = [modifier.object for modifier in mesh_ob.modifiers if modifier.object.type == "ARMATURE"]
        for armature in set(armatures):
            for vertexGroup in mesh_ob.vertex_groups:
                currBone = armature.data.bones.get(vertexGroup.name)
                nextBone = currBone
                while (nextBone != None) and (nextBone.layers[0] == False):
                    nextBone.layers[0] = True
                    nextBone.layers[1] = False
                    nextBone = nextBone.parent

def hideUnusedBones(meshes_obs):
    hideAllBones(meshes_obs)
    moveUsedBoneChain(meshes_obs)

def importArmature():
    bones = xpsData.bones
    boneCount = len(xpsData.bones)
    print('Importing Armature', str(boneCount), 'bones')

    armature_da = bpy.data.armatures.new("Armature")
    armature_da.draw_type = 'STICK'
    armature_ob = bpy.data.objects.new("Armature", armature_da)
    armature_ob.show_x_ray = True;

    bpy.context.scene.objects.link(armature_ob)

    bpy.context.scene.objects.active = armature_ob
    bpy.ops.object.mode_set(mode='EDIT')

    newBoneName()
    #create all Bones
    for bone in bones:
        editBone = armature_ob.data.edit_bones.new(bone.name)
        #Bone index change after parenting. This keeps original index
        addBoneName(editBone.name)

        transformedBone = coordTransform(bone.co)
        editBone.head = Vector(transformedBone)
        setMinumunLenght(editBone)

        #editBone.use_connect = True;

    #set all bone parents
    for bone in bones:
        if (bone.parentId >= 0):
            editBone = armature_da.edit_bones[bone.id]
            editBone.parent = armature_da.edit_bones[bone.parentId]
    markSelected(armature_ob)
    bpy.ops.object.mode_set(mode='OBJECT')
    return armature_ob

def calcCenter(coords):
    sum = None
    for coord in coords:
        if sum == None:
            sum = coord.xyz
        else:
            sum += coord.xyz
    if sum:
        center = sum / len(coords)

    return center

def boneTailMiddle(bones):
    #ChildBone Middle point
    for bone in bones:
        if bone.layers[0]:
            childBones = [childBone for childBone in bone.children if childBone.layers[0]]
        else:
            childBones = [childBone for childBone in bone.children]

        if childBones:
            #Set tail to children middle
            bone.tail = calcCenter([childBone.head for childBone in childBones])
        else:
            #if no child, set tail acording to parent
            if bone.parent != None:
                if bone.head.xyz != bone.parent.tail.xyz:
                    #Tail to diference between bone and parent
                    delta = bone.head.xyz - bone.parent.tail.xyz
                else:
                    #Tail to same lenght/direction than parent
                    delta = bone.parent.tail.xyz - bone.parent.head.xyz
                bone.tail = bone.head.xyz + delta

    #Set minimum bone length
    for bone in bones:
        setMinumunLenght(bone)

def markSelected(ob):
    ob.select = True

def makeUvs(mesh_ob, uvLayers):
    #Create UVLayers
    for i in range(len(uvLayers[0])):
        mesh_ob.uv_textures.new(name="UV" + str(i+1))

    #Assign UVCoords
    for layerIdx, uvLayer in enumerate(mesh_ob.uv_layers):
        for uvVertIdx, uvVert in enumerate(uvLayer.data):
            vertIdx = mesh_ob.loops[uvVertIdx].vertex_index

            uvCoor = uvLayers[vertIdx][layerIdx]
            uvVert.uv = Vector(uvCoor)

def importMeshesList(armature_ob):
    return [importMesh(armature_ob, meshInfo) for meshInfo in xpsData.meshes]

def importMesh(armature_ob, meshInfo):
    boneCount = len(xpsData.bones)
    #Create Mesh
    meshFullName = meshInfo.name
    print()
    print("---*** Importing Mesh " + meshFullName + " ***---")

    #Load UV Layers Count
    uvLayerCount = meshInfo.uvCount
    print("UV Layer Count: " + str(uvLayerCount))

    #Load Textures Count
    textureCount = len(meshInfo.textures)
    print("Texture Count: " + str(textureCount))

    #Load Textures Filepaths and UvLayers
    textureFilepaths = meshInfo.textures

    #Create Mesh
    mesh_ob = makeMesh(meshFullName)
    mesh_da = mesh_ob.data

    coords = []
    normals = []
    vertColors = []
    uvLayers = []
    vrtxList = []
    nbVrtx = []

    for vertex in meshInfo.vertices:
        coords.append(coordTransform(vertex.co))
        normals.append(coordTransform(vertex.norm))
        vertColors.append(vertex.vColor)
        uvLayers.append(uvTransformLayers(vertex.uv))
        vrtxList.append(vertex.boneId)
        nbVrtx.append(vertex.boneWeight)

    #Create Faces
    faces = faceTransformList(meshInfo.faces)
    mesh_da.from_pydata(coords, [], faces)
    mesh_da.polygons.foreach_set("use_smooth", [True] * len(mesh_da.polygons))

    #Make UVLayers
    makeUvs(mesh_da, uvLayers)

    #Make Material
    makeMaterial(mesh_da, meshInfo)

    #Set UV Textures
    setUvTexture(mesh_da)

    setArmatureModifier(armature_ob, mesh_ob)

    makeVertexGroups(mesh_ob, meshInfo)

    #makeBoneGroups
    makeBoneGroups(armature_ob, mesh_ob)

    #mesh_da.update()
    markSelected(mesh_ob)

    return mesh_ob

def setArmatureModifier(armature_ob, mesh_ob):
    mod = mesh_ob.modifiers.new(type="ARMATURE", name="Armature")
    mod.use_vertex_groups = True
    mod.object = armature_ob

def makeVertexGroups(mesh_ob, meshInfo):
    '''Make vertex groups and assign weights'''
    for vertex in meshInfo.vertices:
        for i,boneIdx in enumerate(vertex.boneId):
            vertexWeight = vertex.boneWeight[i]
            if boneIdx != 0 and vertexWeight != 0:
                #blender limits vertexGroupNames to 63 chars

                armatures = getAllArmaturesForMesh(mesh_ob)
                for armature in armatures:
                    #use original index to get current bone name in blender
                    vertexGroupName = getBoneName(boneIdx)
                    bone = armature.data.bones[vertexGroupName]
                    vertGroup = mesh_ob.vertex_groups.get(vertexGroupName)
                    if not vertGroup:
                        vertGroup = mesh_ob.vertex_groups.new(vertexGroupName)
                    vertGroup.add([vertex.id], vertexWeight, 'REPLACE')

def makeBoneGroups(armature_ob, mesh_ob):
    import random
    C = bpy.context
    #Use current theme for selecte and active bone colors
    current_theme = C.user_preferences.themes.items()[0][0]
    theme = C.user_preferences.themes[current_theme]

    #random bone surface color by mesh
    bone_pose_surface_color = (random.random(), random.random(), random.random())
    bone_pose_color = theme.view_3d.bone_pose
    bone_pose_active_color = theme.view_3d.bone_pose_active

    #Store scene mode for later
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
    bvhgroup.color_set='CUSTOM'
    return bvhgroup

if __name__ == "__main__":

    removeUnusedBones = False
    combineMeshes = False
    impDefPose = True

    readfilename0 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - XPS.mesh'
    readfilename1 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - XPS pose.mesh'
    readfilename2 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - BLENDER.mesh'
    readfilename3 = r'G:\3DModeling\XNALara\XNALara_XPS\data\TESTING5\Drake\RECB DRAKE Pack_By DamianHandy\DRAKE Sneaking Suit - Open_by DamianHandy\Generic_Item - BLENDER pose.mesh'

    getInputFilename(readfilename1, removeUnusedBones, combineMeshes,0 ,0, impDefPose)



