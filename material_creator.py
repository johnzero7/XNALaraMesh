# <pep8 compliant>

import bpy
import os
import random
from enum import Enum
from mathutils import Vector
from . import xps_material
from . import xps_const


COLOR_SPACE_NONE = 'Non-Color'
ALPHA_MODE_CHANNEL = 'CHANNEL_PACKED'
# Nodes Layout
NODE_FRAME = 'NodeFrame'

# Nodes Shaders
BSDF_DIFFUSE_NODE = 'ShaderNodeBsdfDiffuse'
BSDF_EMISSION_NODE = 'ShaderNodeEmission'
BSDF_GLOSSY_NODE = 'ShaderNodeBsdfGlossy'
PRINCIPLED_SHADER_NODE = 'ShaderNodeBsdfPrincipled'
BSDF_TRANSPARENT_NODE = 'ShaderNodeBsdfTransparent'
BSDF_GLASS_NODE = 'ShaderNodeBsdfGlass'
SHADER_ADD_NODE = 'ShaderNodeAddShader'
SHADER_MIX_NODE = 'ShaderNodeMixShader'

# Nodes Color
RGB_MIX_NODE = 'ShaderNodeMixRGB'
INVERT_NODE = 'ShaderNodeInvert'

# Nodes Input
TEXTURE_IMAGE_NODE = 'ShaderNodeTexImage'
ENVIRONMENT_IMAGE_NODE = 'ShaderNodeTexEnvironment'
COORD_NODE = 'ShaderNodeTexCoord'

# Nodes Outputs
OUTPUT_NODE = 'ShaderNodeOutputMaterial'

# Nodes Vector
MAPPING_NODE = 'ShaderNodeMapping'
NORMAL_MAP_NODE = 'ShaderNodeNormalMap'

# Nodes Convert
SHADER_NODE_MATH = 'ShaderNodeMath'
RGB_TO_BW_NODE = 'ShaderNodeRGBToBW'
SHADER_NODE_SEPARATE_RGB = 'ShaderNodeSeparateRGB'
SHADER_NODE_COMBINE_RGB = 'ShaderNodeCombineRGB'

# Node Groups
NODE_GROUP = 'ShaderNodeGroup'
NODE_GROUP_INPUT = 'NodeGroupInput'
NODE_GROUP_OUTPUT = 'NodeGroupOutput'
SHADER_NODE_TREE = 'ShaderNodeTree'

# Node Custom Groups
INVERT_CHANNEL_NODE = 'Invert Channel'
MIX_NORMAL_NODE = 'Normal Mix'
NORMAL_MASK_NODE = 'Normal Mask'

# Sockets
NODE_SOCKET_COLOR = 'NodeSocketColor'
NODE_SOCKET_FLOAT = 'NodeSocketFloat'
NODE_SOCKET_FLOAT_FACTOR = 'NodeSocketFloatFactor'
NODE_SOCKET_SHADER = 'NodeSocketShader'
NODE_SOCKET_VECTOR = 'NodeSocketVector'


class TextureType(Enum):
    DIFFUSE = 'diffuse'
    LIGHT = 'lightmap'
    BUMP = 'bumpmap'
    SPECULAR = 'specular'
    ENVIRONMENT = 'enviroment'
    MASK = 'mask'
    BUMP1 = 'bump1'
    BUMP2 = 'bump2'
    EMISSION = 'emission'
    EMISSION_MINI = 'emission_mini_map'


def makeMaterialOutputNode(node_tree):
    node = node_tree.nodes.new(OUTPUT_NODE)
    node.location = 600, 0
    return node


def makePBRShaderNode(node_tree):
    node = node_tree.nodes.new(PRINCIPLED_SHADER_NODE)
    node.location = 200, 0
    return node


def makeImageNode(node_tree):
    node = node_tree.nodes.new(TEXTURE_IMAGE_NODE)
    node.location = -400, 0
    return node


def makeEnvironmentNode(node_tree):
    node = node_tree.nodes.new(ENVIRONMENT_IMAGE_NODE)
    node.location = -400, 0
    return node


def makeTransparencyNode(node_tree):
    node = node_tree.nodes.new(BSDF_TRANSPARENT_NODE)
    node.location = -400, -200
    return node


def makeShaderMixNode(node_tree):
    node = node_tree.nodes.new(SHADER_MIX_NODE)
    node.location = -400, -400
    return node


def randomColor():
    randomR = random.random()
    randomG = random.random()
    randomB = random.random()
    return (randomR, randomG, randomB)


def randomColorRanged():
    r = random.uniform(.5, 1)
    g = random.uniform(.5, 1)
    b = random.uniform(.5, 1)
    return (r, g, b)


def makeImageFilepath(rootDir, textureFilename):
    return os.path.join(rootDir, textureFilename)


def loadImage(textureFilepath):
    textureFilename = os.path.basename(textureFilepath)
    fileRoot, fileExt = os.path.splitext(textureFilename)

    if (os.path.exists(textureFilepath)):
        print("Loading Texture: " + textureFilename)
        image = bpy.data.images.load(filepath=textureFilepath, check_existing=True)
    else:
        print("Warning. Texture not found " + textureFilename)
        image = bpy.data.images.new(
            name=textureFilename, width=1024, height=1024, alpha=True,
            float_buffer=False)
        image.source = 'FILE'
        image.filepath = textureFilepath
    image.alpha_mode = ALPHA_MODE_CHANNEL

    return image


def newTextureSlot(materialData):
    textureSlot = materialData.texture_slots.add()
    textureSlot.texture_coords = "UV"
    # textureSlot.texture = imgTex
    textureSlot.use_map_alpha = True
    textureSlot.alpha_factor = 1.0
    return textureSlot


def makeMaterial(xpsSettings, rootDir, mesh_da, meshInfo, flags):
    # Create the material for BI & Nodes
    meshFullName = meshInfo.name
    materialData = bpy.data.materials.new(meshFullName)
    mesh_da.materials.append(materialData)

    # Create
    makeNodesMaterial(xpsSettings, materialData, rootDir, mesh_da, meshInfo, flags)


def makeNodesMaterial(xpsSettings, materialData, rootDir, mesh_da, meshInfo, flags):
    textureFilepaths = meshInfo.textures
    materialData.use_nodes = True
    node_tree = materialData.node_tree
    node_tree.nodes.clear()

    meshFullName = materialData.name
    renderType = xps_material.makeRenderType(meshFullName)
    renderGroup = xps_material.RenderGroup(renderType)
    param1 = renderType.texRepeater1
    param2 = renderType.texRepeater2
    strengthFac = renderType.specularity

    useAlpha = renderGroup.rgAlpha

    # Nodes
    ouputNode = makeMaterialOutputNode(node_tree)
    shaderNode = makePBRShaderNode(node_tree)
    node_tree.links.new(shaderNode.outputs['BSDF'], ouputNode.inputs['Surface'])
    ouputNode.location = shaderNode.location + Vector((700, 400))
    coordNode = node_tree.nodes.new(COORD_NODE)

    if useAlpha:
        materialData.blend_method = 'BLEND'
        # materialData.show_transparent_backside = False
        transparentNode = makeTransparencyNode(node_tree)
        transparentNode.location = shaderNode.location + Vector((300, 250))
        shaderMixNode = makeShaderMixNode(node_tree)
        shaderMixNode.location = shaderNode.location + Vector((500, 400))
        node_tree.links.new(shaderMixNode.outputs['Shader'], ouputNode.inputs['Surface'])
        node_tree.links.new(transparentNode.outputs['BSDF'], shaderMixNode.inputs[1])
        node_tree.links.new(shaderNode.outputs['BSDF'], shaderMixNode.inputs[2])

    bump1Image = None
    bump2Image = None
    maskGroupNode = None
    normalMixNode = None
    diffuseImgNode = None
    normalMapNode = None

    col_width = 200
    imagesPosX = -col_width * 6
    imagesPosY = 400

    imageFilepath = None
    for texIndex, textureInfo in enumerate(textureFilepaths):
        textureFilename = textureInfo.file
        # textureUvLayer = textureInfo.uvLayer
        textureBasename = os.path.basename(textureFilename)

        # image mapping node
        mappingCoordNode = node_tree.nodes.new(MAPPING_NODE)
        # load image
        imageFilepath = makeImageFilepath(rootDir, textureBasename)
        imageNode = makeImageNode(node_tree)
        imageNode.image = loadImage(imageFilepath)
        node_tree.links.new(mappingCoordNode.outputs['Vector'], imageNode.inputs['Vector'])
        imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * 0))
        mappingCoordNode.location = imageNode.location + Vector((-400, 0))
        node_tree.links.new(coordNode.outputs['UV'], mappingCoordNode.inputs['Vector'])

        if texIndex < len(renderGroup.rgTexType):
            texType = TextureType(renderGroup.rgTexType[texIndex])

        if (texType == TextureType.DIFFUSE):
            imageNode.label = 'Diffuse'
            node_tree.links.new(imageNode.outputs['Color'], shaderNode.inputs['Base Color'])
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * 1))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            diffuseImgNode = imageNode
            if useAlpha:
                node_tree.links.new(imageNode.outputs['Alpha'], shaderMixNode.inputs['Fac'])
        elif (texType == TextureType.LIGHT):
            imageNode.label = 'Light Map'
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * 0))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            aoMixNode = node_tree.nodes.new(RGB_MIX_NODE)
            aoMixNode.location = imageNode.location + Vector((400, 100))
            aoMixNode.blend_type = 'MULTIPLY'
            aoMixNode.inputs['Fac'].default_value = 1
            node_tree.links.new(diffuseImgNode.outputs['Color'], aoMixNode.inputs[1])
            node_tree.links.new(imageNode.outputs['Color'], aoMixNode.inputs[2])
            node_tree.links.new(aoMixNode.outputs['Color'], shaderNode.inputs['Base Color'])
        elif (texType == TextureType.BUMP):
            imageNode.label = 'Bump Map'
            imageNode.image.colorspace_settings.name = COLOR_SPACE_NONE
            normalMapNode = node_tree.nodes.new(NORMAL_MAP_NODE)
            normalChannelsGroupNode = node_tree.nodes.new(NODE_GROUP)
            normalChannelsGroupNode.node_tree = bpy.data.node_groups[INVERT_CHANNEL_NODE]
            normalChannelsGroupNode.inputs['R'].default_value = flags[xps_const.TANGENT_SPACE_RED]
            normalChannelsGroupNode.inputs['G'].default_value = flags[xps_const.TANGENT_SPACE_GREEN]
            normalChannelsGroupNode.inputs['B'].default_value = flags[xps_const.TANGENT_SPACE_BLUE]
            node_tree.links.new(imageNode.outputs['Color'], normalChannelsGroupNode.inputs['Color'])
            node_tree.links.new(normalChannelsGroupNode.outputs['Color'], normalMapNode.inputs['Color'])
            node_tree.links.new(normalMapNode.outputs['Normal'], shaderNode.inputs['Normal'])
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * -2))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            normalChannelsGroupNode.location = imageNode.location + Vector((col_width * 1.5, 0))
            normalMapNode.location = imageNode.location + Vector((col_width * 5, 0))
        elif (texType == TextureType.SPECULAR):
            imageNode.label = 'Specular'
            imageNode.image.colorspace_settings.name = COLOR_SPACE_NONE
            rgbToBwNode = node_tree.nodes.new(RGB_TO_BW_NODE)
            # Math node to power texture
            mathNode = node_tree.nodes.new(SHADER_NODE_MATH)
            mathNode.inputs[1].default_value = 2
            mathNode.operation = 'POWER'
            invertNode = node_tree.nodes.new(INVERT_NODE)
            node_tree.links.new(imageNode.outputs['Color'], rgbToBwNode.inputs['Color'])
            node_tree.links.new(rgbToBwNode.outputs['Val'], mathNode.inputs[0])
            node_tree.links.new(mathNode.outputs['Value'], invertNode.inputs['Color'])
            node_tree.links.new(invertNode.outputs['Color'], shaderNode.inputs['Roughness'])
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * -1))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            rgbToBwNode.location = imageNode.location + Vector((col_width * 1.5, 0))
            mathNode.location = rgbToBwNode.location + Vector((col_width, 0))
            invertNode.location = mathNode.location + Vector((col_width, 0))
        elif (texType == TextureType.ENVIRONMENT):
            imageNode.label = 'Reflection'
            # insert add-shader node
            shaderAddNode = node_tree.nodes.new(SHADER_ADD_NODE)
            shaderAddNode.location = shaderNode.location + Vector((300, 100))
            from_socket = shaderNode.outputs['BSDF'].links[0].from_socket
            to_socket = shaderNode.outputs['BSDF'].links[0].to_socket
            node_tree.links.new(from_socket, shaderAddNode.inputs[1])
            node_tree.links.new(shaderAddNode.outputs['Shader'], to_socket)
            # Swap image -> environment
            environmentNode = makeEnvironmentNode(node_tree)
            # replace links
            from_socket = imageNode.inputs['Vector'].links[0].from_socket
            to_socket = imageNode.inputs['Vector'].links[0].to_socket
            node_tree.links.new(from_socket, environmentNode.inputs['Vector'])
            environmentNode.image = imageNode.image
            node_tree.nodes.remove(imageNode)
            imageNode = environmentNode
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * 2))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            node_tree.links.new(coordNode.outputs['Reflection'], mappingCoordNode.inputs['Vector'])

            # Emission
            emissionNode = node_tree.nodes.new(BSDF_EMISSION_NODE)
            emissionNode.inputs['Strength'].default_value = strengthFac
            emissionNode.location = shaderNode.location + Vector((0, 150))
            node_tree.links.new(imageNode.outputs['Color'], emissionNode.inputs['Color'])
            node_tree.links.new(emissionNode.outputs['Emission'], shaderAddNode.inputs[0])
        elif (texType == TextureType.MASK):
            imageNode.label = 'Bump Mask'
            imageNode.image.colorspace_settings.name = COLOR_SPACE_NONE
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * -4))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            maskGroupNode = node_tree.nodes.new(NODE_GROUP)
            maskGroupNode.node_tree = bpy.data.node_groups[NORMAL_MASK_NODE]
            maskGroupNode.location = imageNode.location + Vector((col_width * 2.5, 0))
            node_tree.links.new(imageNode.outputs['Color'], maskGroupNode.inputs['Mask'])

        elif (texType == TextureType.BUMP1):
            imageNode.label = 'Micro Bump 1'
            imageNode.image.colorspace_settings.name = COLOR_SPACE_NONE
            texRepeater = None
            if renderGroup.renderGroupNum in (28, 29):
                texRepeater = renderType.texRepeater2
            else:
                texRepeater = renderType.texRepeater1

            mappingCoordNode.scale = (texRepeater, texRepeater, texRepeater)
            channelsGroupNode = node_tree.nodes.new(NODE_GROUP)
            channelsGroupNode.node_tree = bpy.data.node_groups[INVERT_CHANNEL_NODE]
            channelsGroupNode.inputs['G'].default_value = 1
            node_tree.links.new(coordNode.outputs['UV'], mappingCoordNode.inputs['Vector'])
            node_tree.links.new(mappingCoordNode.outputs['Vector'], imageNode.inputs['Vector'])
            node_tree.links.new(imageNode.outputs['Color'], channelsGroupNode.inputs['Color'])
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * -3))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            channelsGroupNode.location = imageNode.location + Vector((col_width * 1.5, 0))
            bump1Image = channelsGroupNode
        elif (texType == TextureType.BUMP2):
            imageNode.label = 'Micro Bump 2'
            imageNode.image.colorspace_settings.name = COLOR_SPACE_NONE
            texRepeater = renderType.texRepeater2
            mappingCoordNode.scale = (texRepeater, texRepeater, texRepeater)
            channelsGroupNode = node_tree.nodes.new(NODE_GROUP)
            channelsGroupNode.node_tree = bpy.data.node_groups[INVERT_CHANNEL_NODE]
            channelsGroupNode.inputs['G'].default_value = 1
            node_tree.links.new(coordNode.outputs['UV'], mappingCoordNode.inputs['Vector'])
            node_tree.links.new(mappingCoordNode.outputs['Vector'], imageNode.inputs['Vector'])
            node_tree.links.new(imageNode.outputs['Color'], channelsGroupNode.inputs['Color'])
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * -5))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            channelsGroupNode.location = imageNode.location + Vector((col_width * 1.5, 0))
            bump2Image = channelsGroupNode
        elif (texType == TextureType.EMISSION):
            imageNode.label = 'Emission Map'
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * 2))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            # insert add-shader
            shaderAddNode = node_tree.nodes.new(SHADER_ADD_NODE)
            shaderAddNode.location = shaderNode.location + Vector((300, 100))
            from_socket = shaderNode.outputs['BSDF'].links[0].from_socket
            to_socket = shaderNode.outputs['BSDF'].links[0].to_socket
            node_tree.links.new(from_socket, shaderAddNode.inputs[1])
            node_tree.links.new(shaderAddNode.outputs['Shader'], to_socket)

            # Emission
            emissionNode = node_tree.nodes.new(BSDF_EMISSION_NODE)
            emissionNode.location = shaderNode.location + Vector((0, 150))
            node_tree.links.new(imageNode.outputs['Color'], emissionNode.inputs['Color'])
            node_tree.links.new(emissionNode.outputs['Emission'], shaderAddNode.inputs[0])

        elif (texType == TextureType.EMISSION_MINI):
            imageNode.label = 'Mini Emission'
            imageNode.location = shaderNode.location + Vector((imagesPosX, imagesPosY * 3))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            mappingCoordNode.scale = (param1, param1, param1)
            # insert add-shader
            shaderAddNode = node_tree.nodes.new(SHADER_ADD_NODE)
            shaderAddNode.location = shaderNode.location + Vector((300, 100))
            from_socket = shaderNode.outputs['BSDF'].links[0].from_socket
            to_socket = shaderNode.outputs['BSDF'].links[0].to_socket
            node_tree.links.new(from_socket, shaderAddNode.inputs[1])
            node_tree.links.new(shaderAddNode.outputs['Shader'], to_socket)

            # Emission
            emissionNode = node_tree.nodes.new(BSDF_EMISSION_NODE)
            emissionNode.location = shaderNode.location + Vector((0, 150))
            node_tree.links.new(imageNode.outputs['Color'], emissionNode.inputs['Color'])
            node_tree.links.new(emissionNode.outputs['Emission'], shaderAddNode.inputs[0])

    if diffuseImgNode:
        coordNode.location = diffuseImgNode.location + Vector((-1000, 0))

    if bump1Image:
        node_tree.links.new(bump1Image.outputs['Color'], maskGroupNode.inputs[1])
        normalMixNode = node_tree.nodes.new(NODE_GROUP)
        normalMixNode.node_tree = bpy.data.node_groups[MIX_NORMAL_NODE]
        # normalMapNode.location = bump1Image.location + Vector((400, 0))
        normalMixNode.location = normalMapNode.location + Vector((-200, 0))
        node_tree.links.new(normalChannelsGroupNode.outputs['Color'], normalMixNode.inputs['Main'])
        node_tree.links.new(normalMixNode.outputs['Color'], normalMapNode.inputs['Color'])
        node_tree.links.new(bump1Image.outputs['Color'], maskGroupNode.inputs['Normal1'])

    if bump2Image:
        node_tree.links.new(bump2Image.outputs['Color'], maskGroupNode.inputs['Normal2'])
    if normalMixNode and maskGroupNode:
        node_tree.links.new(maskGroupNode.outputs['Normal'], normalMixNode.inputs['Detail'])

    # channelsGroupNodex = node_tree.nodes.new(NODE_GROUP)
    # channelsGroupNodex.node_tree = bpy.data.node_groups[INVERT_CHANNEL_NODE]

    # maskGroupNodex = node_tree.nodes.new(NODE_GROUP)
    # maskGroupNodex.node_tree = bpy.data.node_groups[NORMAL_MASK_NODE]


def mix_normal_group():
    # create a group
    if MIX_NORMAL_NODE in bpy.data.node_groups:
        return
    bpy.data.node_groups.new(MIX_NORMAL_NODE, SHADER_NODE_TREE)
    node_tree = bpy.data.node_groups.get(MIX_NORMAL_NODE)
    node_tree.nodes.clear()

    mainNormalSeparateNode = node_tree.nodes.new(SHADER_NODE_SEPARATE_RGB)
    mainNormalSeparateNode.location = Vector((0, 0))
    detailNormalSeparateNode = node_tree.nodes.new(SHADER_NODE_SEPARATE_RGB)
    detailNormalSeparateNode.location = mainNormalSeparateNode.location + Vector((0, -200))
    mainNormalCombineNode = node_tree.nodes.new(SHADER_NODE_COMBINE_RGB)
    mainNormalCombineNode.location = mainNormalSeparateNode.location + Vector((200, 0))
    detailNormalCombineNode = node_tree.nodes.new(SHADER_NODE_COMBINE_RGB)
    detailNormalCombineNode.location = mainNormalSeparateNode.location + Vector((200, -200))

    multiplyBlueNode = node_tree.nodes.new(SHADER_NODE_MATH)
    multiplyBlueNode.operation = 'MULTIPLY'
    multiplyBlueNode.inputs[1].default_value = 1
    multiplyBlueNode.location = mainNormalSeparateNode.location + Vector((200, -400))

    addRGBNode = node_tree.nodes.new(RGB_MIX_NODE)
    addRGBNode.blend_type = 'ADD'
    addRGBNode.inputs['Fac'].default_value = 1
    addRGBNode.location = mainNormalSeparateNode.location + Vector((400, 0))

    subsRGBNode = node_tree.nodes.new(RGB_MIX_NODE)
    subsRGBNode.blend_type = 'SUBTRACT'
    subsRGBNode.inputs['Fac'].default_value = 1
    subsRGBNode.location = mainNormalSeparateNode.location + Vector((600, -100))

    separateRedBlueNode = node_tree.nodes.new(SHADER_NODE_SEPARATE_RGB)
    separateRedBlueNode.location = mainNormalSeparateNode.location + Vector((800, -100))
    combineFinalNode = node_tree.nodes.new(SHADER_NODE_COMBINE_RGB)
    combineFinalNode.location = mainNormalSeparateNode.location + Vector((1000, -200))

    # Input/Output
    group_inputs = node_tree.nodes.new(NODE_GROUP_INPUT)
    group_inputs.location = mainNormalSeparateNode.location + Vector((-200, -100))
    group_outputs = node_tree.nodes.new(NODE_GROUP_OUTPUT)
    group_outputs.location = mainNormalSeparateNode.location + Vector((1200, -100))
    node_tree.inputs.clear()
    node_tree.outputs.clear()

    # Input Sockets
    main_normal_socket = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Main')
    main_normal_socket.default_value = (.5, .5, 1, 1)
    detail_normal_socket = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Detail')
    detail_normal_socket.default_value = (.5, .5, 1, 1)

    # Output Sockets
    output_value = node_tree.outputs.new(NODE_SOCKET_COLOR, 'Color')

    # Links Input
    links = node_tree.links
    links.new(group_inputs.outputs['Main'], mainNormalSeparateNode.inputs['Image'])
    links.new(group_inputs.outputs['Detail'], detailNormalSeparateNode.inputs['Image'])

    links.new(mainNormalSeparateNode.outputs['R'], mainNormalCombineNode.inputs['R'])
    links.new(mainNormalSeparateNode.outputs['G'], mainNormalCombineNode.inputs['G'])
    links.new(mainNormalSeparateNode.outputs['B'], multiplyBlueNode.inputs[0])
    links.new(detailNormalSeparateNode.outputs['R'], detailNormalCombineNode.inputs['R'])
    links.new(detailNormalSeparateNode.outputs['G'], detailNormalCombineNode.inputs['G'])
    links.new(detailNormalSeparateNode.outputs['B'], multiplyBlueNode.inputs[1])

    links.new(mainNormalCombineNode.outputs['Image'], addRGBNode.inputs[1])
    links.new(detailNormalCombineNode.outputs['Image'], addRGBNode.inputs[2])
    links.new(addRGBNode.outputs['Color'], subsRGBNode.inputs[1])

    links.new(subsRGBNode.outputs['Color'], separateRedBlueNode.inputs['Image'])

    links.new(separateRedBlueNode.outputs['R'], combineFinalNode.inputs['R'])
    links.new(separateRedBlueNode.outputs['G'], combineFinalNode.inputs['G'])
    links.new(multiplyBlueNode.outputs['Value'], combineFinalNode.inputs['B'])

    links.new(combineFinalNode.outputs['Image'], group_outputs.inputs['Color'])

    return node_tree


def invert_channel_group():
    # create a group
    if INVERT_CHANNEL_NODE in bpy.data.node_groups:
        return
    bpy.data.node_groups.new(INVERT_CHANNEL_NODE, SHADER_NODE_TREE)
    node_tree = bpy.data.node_groups.get(INVERT_CHANNEL_NODE)
    node_tree.nodes.clear()

    separateRgbNode = node_tree.nodes.new(SHADER_NODE_SEPARATE_RGB)
    separateRgbNode.location = Vector((0, 0))

    invertRNode = node_tree.nodes.new(INVERT_NODE)
    invertRNode.inputs[0].default_value = 0
    invertRNode.location = separateRgbNode.location + Vector((200, 40))
    invertGNode = node_tree.nodes.new(INVERT_NODE)
    invertGNode.inputs[0].default_value = 1
    invertGNode.location = separateRgbNode.location + Vector((200, -60))
    invertBNode = node_tree.nodes.new(INVERT_NODE)
    invertBNode.inputs[0].default_value = 0
    invertBNode.location = separateRgbNode.location + Vector((200, -160))

    combineRgbNode = node_tree.nodes.new(SHADER_NODE_COMBINE_RGB)
    combineRgbNode.location = separateRgbNode.location + Vector((600, 0))

    # Input/Output
    group_inputs = node_tree.nodes.new(NODE_GROUP_INPUT)
    group_inputs.location = separateRgbNode.location + Vector((-200, -100))
    group_outputs = node_tree.nodes.new(NODE_GROUP_OUTPUT)
    group_outputs.location = combineRgbNode.location + Vector((200, 0))
    node_tree.inputs.clear()
    node_tree.outputs.clear()

    # Input/Output Sockets
    input_color = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Color')
    input_color.default_value = (.5, .5, .5, 1)
    invert_r = node_tree.inputs.new(NODE_SOCKET_FLOAT_FACTOR, 'R')
    invert_r.default_value = 0
    invert_r.min_value = 0
    invert_r.max_value = 1
    invert_g = node_tree.inputs.new(NODE_SOCKET_FLOAT_FACTOR, 'G')
    invert_g.default_value = 0
    invert_g.min_value = 0
    invert_g.max_value = 1
    invert_b = node_tree.inputs.new(NODE_SOCKET_FLOAT_FACTOR, 'B')
    invert_b.default_value = 0
    invert_b.min_value = 0
    invert_b.max_value = 1

    output_value = node_tree.outputs.new(NODE_SOCKET_COLOR, 'Color')

    # Links Input
    links = node_tree.links
    links.new(group_inputs.outputs['Color'], separateRgbNode.inputs['Image'])
    links.new(group_inputs.outputs['R'], invertRNode.inputs['Fac'])
    links.new(group_inputs.outputs['G'], invertGNode.inputs['Fac'])
    links.new(group_inputs.outputs['B'], invertBNode.inputs['Fac'])
    links.new(separateRgbNode.outputs['R'], invertRNode.inputs['Color'])
    links.new(separateRgbNode.outputs['G'], invertGNode.inputs['Color'])
    links.new(separateRgbNode.outputs['B'], invertBNode.inputs['Color'])

    links.new(invertRNode.outputs['Color'], combineRgbNode.inputs['R'])
    links.new(invertGNode.outputs['Color'], combineRgbNode.inputs['G'])
    links.new(invertBNode.outputs['Color'], combineRgbNode.inputs['B'])

    links.new(combineRgbNode.outputs['Image'], group_outputs.inputs['Color'])

    return node_tree


def normal_mask_group():
    # create a group
    if NORMAL_MASK_NODE in bpy.data.node_groups:
        return
    bpy.data.node_groups.new(NORMAL_MASK_NODE, SHADER_NODE_TREE)
    node_tree = bpy.data.node_groups.get(NORMAL_MASK_NODE)
    node_tree.nodes.clear()

    maskSeparateNode = node_tree.nodes.new(SHADER_NODE_SEPARATE_RGB)
    # maskSeparateNode.location = imageNode.location + Vector((200, -60))

    # Mask Red Channel
    maskRedPowerNode = node_tree.nodes.new(SHADER_NODE_MATH)
    maskRedPowerNode.operation = 'POWER'
    maskRedPowerNode.inputs[1].default_value = .4
    maskRedPowerNode.location = maskSeparateNode.location + Vector((200, 100))

    maskMixRedNode = node_tree.nodes.new(RGB_MIX_NODE)
    maskMixRedNode.blend_type = 'MIX'
    maskMixRedNode.inputs[1].default_value = ((.5, .5, 1, 1))
    maskMixRedNode.location = maskRedPowerNode.location + Vector((200, 100))

    # Mask Green Channel
    maskGreenPowerNode = node_tree.nodes.new(SHADER_NODE_MATH)
    maskGreenPowerNode.operation = 'POWER'
    maskGreenPowerNode.inputs[1].default_value = .4
    maskGreenPowerNode.location = maskSeparateNode.location + Vector((200, -100))

    maskMixGreenNode = node_tree.nodes.new(RGB_MIX_NODE)
    maskMixGreenNode.blend_type = 'MIX'
    maskMixGreenNode.inputs[1].default_value = ((.5, .5, 1, 1))
    maskMixGreenNode.location = maskGreenPowerNode.location + Vector((200, -100))

    # Mix Masked Normals
    normalMixNode = node_tree.nodes.new(NODE_GROUP)
    normalMixNode.node_tree = bpy.data.node_groups[MIX_NORMAL_NODE]
    normalMixNode.location = maskSeparateNode.location + Vector((600, 0))

    node_tree.links.new(maskSeparateNode.outputs['R'], maskRedPowerNode.inputs[0])
    node_tree.links.new(maskSeparateNode.outputs['G'], maskGreenPowerNode.inputs[0])
    node_tree.links.new(maskRedPowerNode.outputs['Value'], maskMixRedNode.inputs[0])
    node_tree.links.new(maskGreenPowerNode.outputs['Value'], maskMixGreenNode.inputs[0])
    node_tree.links.new(maskMixRedNode.outputs['Color'], normalMixNode.inputs['Main'])
    node_tree.links.new(maskMixGreenNode.outputs['Color'], normalMixNode.inputs['Detail'])

    # Input/Output
    group_inputs = node_tree.nodes.new(NODE_GROUP_INPUT)
    group_inputs.location = maskSeparateNode.location + Vector((-200, -100))
    group_outputs = node_tree.nodes.new(NODE_GROUP_OUTPUT)
    group_outputs.location = normalMixNode.location + Vector((200, 0))
    node_tree.inputs.clear()
    node_tree.outputs.clear()

    # Input/Output Sockets
    mask_color = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Mask')
    mask_color.default_value = (1, 1, 1, 1)
    normalMain_color = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Normal1')
    normalMain_color.default_value = (.5, .5, 1, 1)
    normalDetail_color = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Normal2')
    normalDetail_color.default_value = (.5, .5, 1, 1)

    output_value = node_tree.outputs.new(NODE_SOCKET_COLOR, 'Normal')

    # Link Inputs/Output
    node_tree.links.new(group_inputs.outputs['Mask'], maskSeparateNode.inputs['Image'])
    node_tree.links.new(group_inputs.outputs['Normal1'], maskMixRedNode.inputs[2])
    node_tree.links.new(group_inputs.outputs['Normal2'], maskMixGreenNode.inputs[2])
    node_tree.links.new(normalMixNode.outputs['Color'], group_outputs.inputs['Normal'])


def create_group_nodes():
    mix_normal_group()
    invert_channel_group()
    normal_mask_group()
