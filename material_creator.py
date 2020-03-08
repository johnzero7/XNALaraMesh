# <pep8 compliant>

import bpy
import os
import random
from mathutils import Vector
from . import xps_material
from . import xps_const


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
XPS_SHADER_NODE = 'XPS Shader'

# Sockets
NODE_SOCKET_COLOR = 'NodeSocketColor'
NODE_SOCKET_FLOAT = 'NodeSocketFloat'
NODE_SOCKET_FLOAT_FACTOR = 'NodeSocketFloatFactor'
NODE_SOCKET_SHADER = 'NodeSocketShader'
NODE_SOCKET_VECTOR = 'NodeSocketVector'

# Colors
DIFFUSE_COLOR = (0.9, 0.9, 0.9, 1)
SPECULAR_COLOR = (0.707, 0.707, 0.707, 1)
LIGHTMAP_COLOR = (1, 1, 1, 1)
NORMAL_COLOR = (0.5, 0.5, 1, 1)
GREY_COLOR = (0.5, 0.5, 0.5, 1)


def makeMaterialOutputNode(node_tree):
    node = node_tree.nodes.new(OUTPUT_NODE)
    node.location = 600, 0
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


def setNodeScale(node, value):
    # Change from 2.80 to 2.81
    if 'Scale' in node.inputs:
        node.inputs['Scale'].default_value = (value, value, value)
    else:
        node.scale = (value, value, value)


def getNodeGroup(node_tree, group):
    node = node_tree.nodes.new(NODE_GROUP)
    node.node_tree = bpy.data.node_groups[group]
    return node


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
    # Create the material for Nodes
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
    xpsShadeNode = getNodeGroup(node_tree, XPS_SHADER_NODE)
    ouputNode.location = xpsShadeNode.location + Vector((700, 400))
    coordNode = node_tree.nodes.new(COORD_NODE)
    coordNode.location = xpsShadeNode.location + Vector((-2500, 400))

    if useAlpha:
        materialData.blend_method = 'BLEND'

    node_tree.links.new(xpsShadeNode.outputs['Shader'], ouputNode.inputs['Surface'])

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
        imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * 0))
        mappingCoordNode.location = imageNode.location + Vector((-400, 0))
        node_tree.links.new(coordNode.outputs['UV'], mappingCoordNode.inputs['Vector'])

        if texIndex >= len(renderGroup.rgTexType):
            continue

        texType = xps_material.TextureType(renderGroup.rgTexType[texIndex])
        if (texType == xps_material.TextureType.DIFFUSE):
            imageNode.label = 'Diffuse'
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Diffuse'])
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * 1))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            diffuseImgNode = imageNode
            if useAlpha:
                node_tree.links.new(imageNode.outputs['Alpha'], xpsShadeNode.inputs['Alpha'])
        elif (texType == xps_material.TextureType.LIGHT):
            imageNode.label = 'Light Map'
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * 0))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Lightmap'])
        elif (texType == xps_material.TextureType.BUMP):
            imageNode.label = 'Bump Map'
            imageNode.image.colorspace_settings.is_data = True
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Bump Map'])
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * -2))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
        elif (texType == xps_material.TextureType.SPECULAR):
            imageNode.label = 'Specular'
            imageNode.image.colorspace_settings.is_data = True
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Specular'])
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * -1))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
        elif (texType == xps_material.TextureType.ENVIRONMENT):
            imageNode.label = 'Reflection'
            environmentNode = makeEnvironmentNode(node_tree)
            environmentNode.image = imageNode.image
            node_tree.nodes.remove(imageNode)
            imageNode = environmentNode
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * 2))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            node_tree.links.new(coordNode.outputs['Reflection'], mappingCoordNode.inputs['Vector'])
            node_tree.links.new(mappingCoordNode.outputs['Vector'], environmentNode.inputs['Vector'])
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Environment'])
        elif (texType == xps_material.TextureType.MASK):
            imageNode.label = 'Bump Mask'
            imageNode.image.colorspace_settings.is_data = True
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * -3))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Bump Mask'])
        elif (texType == xps_material.TextureType.BUMP1):
            imageNode.label = 'Micro Bump 1'
            imageNode.image.colorspace_settings.is_data = True
            texRepeater = None
            if renderGroup.renderGroupNum in (28, 29):
                texRepeater = renderType.texRepeater2
            else:
                texRepeater = renderType.texRepeater1
            setNodeScale(mappingCoordNode, texRepeater)
            node_tree.links.new(coordNode.outputs['UV'], mappingCoordNode.inputs['Vector'])
            node_tree.links.new(mappingCoordNode.outputs['Vector'], imageNode.inputs['Vector'])
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['MicroBump 1'])
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * -4))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
        elif (texType == xps_material.TextureType.BUMP2):
            imageNode.label = 'Micro Bump 2'
            imageNode.image.colorspace_settings.is_data = True
            texRepeater = renderType.texRepeater2
            setNodeScale(mappingCoordNode, texRepeater)
            node_tree.links.new(coordNode.outputs['UV'], mappingCoordNode.inputs['Vector'])
            node_tree.links.new(mappingCoordNode.outputs['Vector'], imageNode.inputs['Vector'])
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['MicroBump 2'])
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * -5))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
        elif (texType == xps_material.TextureType.EMISSION):
            imageNode.label = 'Emission Map'
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * 2))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Emission'])
        elif (texType == xps_material.TextureType.EMISSION_MINI):
            imageNode.label = 'Mini Emission'
            imageNode.location = xpsShadeNode.location + Vector((imagesPosX, imagesPosY * -6))
            mappingCoordNode.location = imageNode.location + Vector((-400, 0))
            setNodeScale(mappingCoordNode, param1)
            node_tree.links.new(imageNode.outputs['Color'], xpsShadeNode.inputs['Emission'])


def mix_normal_group():
    # create a group
    if MIX_NORMAL_NODE in bpy.data.node_groups:
        return bpy.data.node_groups[MIX_NORMAL_NODE]
    node_tree = bpy.data.node_groups.new(name=MIX_NORMAL_NODE, type=SHADER_NODE_TREE)
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
    main_normal_socket.default_value = NORMAL_COLOR
    detail_normal_socket = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Detail')
    detail_normal_socket.default_value = NORMAL_COLOR

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
        return bpy.data.node_groups[INVERT_CHANNEL_NODE]
    node_tree = bpy.data.node_groups.new(name=INVERT_CHANNEL_NODE, type=SHADER_NODE_TREE)
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
    input_color.default_value = GREY_COLOR
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
        return bpy.data.node_groups[NORMAL_MASK_NODE]
    node_tree = bpy.data.node_groups.new(name=NORMAL_MASK_NODE, type=SHADER_NODE_TREE)
    node_tree.nodes.clear()

    maskSeparateNode = node_tree.nodes.new(SHADER_NODE_SEPARATE_RGB)

    # Mask Red Channel
    maskRedPowerNode = node_tree.nodes.new(SHADER_NODE_MATH)
    maskRedPowerNode.operation = 'POWER'
    maskRedPowerNode.inputs[1].default_value = 1
    maskRedPowerNode.location = maskSeparateNode.location + Vector((200, 100))

    maskMixRedNode = node_tree.nodes.new(RGB_MIX_NODE)
    maskMixRedNode.blend_type = 'MIX'
    maskMixRedNode.inputs[1].default_value = (NORMAL_COLOR)
    maskMixRedNode.location = maskRedPowerNode.location + Vector((200, 100))

    # Mask Green Channel
    maskGreenPowerNode = node_tree.nodes.new(SHADER_NODE_MATH)
    maskGreenPowerNode.operation = 'POWER'
    maskGreenPowerNode.inputs[1].default_value = 1
    maskGreenPowerNode.location = maskSeparateNode.location + Vector((200, -100))

    maskMixGreenNode = node_tree.nodes.new(RGB_MIX_NODE)
    maskMixGreenNode.blend_type = 'MIX'
    maskMixGreenNode.inputs[1].default_value = (NORMAL_COLOR)
    maskMixGreenNode.location = maskGreenPowerNode.location + Vector((200, -100))

    # Mix Masked Normals
    normalMixNode = getNodeGroup(node_tree, MIX_NORMAL_NODE)
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
    mask_color.default_value = LIGHTMAP_COLOR
    normalMain_color = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Normal1')
    normalMain_color.default_value = NORMAL_COLOR
    normalDetail_color = node_tree.inputs.new(NODE_SOCKET_COLOR, 'Normal2')
    normalDetail_color.default_value = NORMAL_COLOR

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
    xps_shader_group()


def xps_shader_group():
    # create a group
    if XPS_SHADER_NODE in bpy.data.node_groups:
        return bpy.data.node_groups[XPS_SHADER_NODE]
    shader = bpy.data.node_groups.new(name=XPS_SHADER_NODE, type=SHADER_NODE_TREE)

    # Group inputs
    group_input = shader.nodes.new(NODE_GROUP_INPUT)
    group_input.location += Vector((-1200, 0))

    group_output = shader.nodes.new(NODE_GROUP_OUTPUT)
    group_output.location += Vector((600, 0))

    output_diffuse = shader.inputs.new(NODE_SOCKET_COLOR, 'Diffuse')
    output_diffuse.default_value = (DIFFUSE_COLOR)
    output_lightmap = shader.inputs.new(NODE_SOCKET_COLOR, 'Lightmap')
    output_lightmap.default_value = (LIGHTMAP_COLOR)
    output_specular = shader.inputs.new(NODE_SOCKET_COLOR, 'Specular')
    output_specular.default_value = (SPECULAR_COLOR)
    output_emission = shader.inputs.new(NODE_SOCKET_COLOR, 'Emission')
    output_normal = shader.inputs.new(NODE_SOCKET_COLOR, 'Bump Map')
    output_normal.default_value = (NORMAL_COLOR)
    output_bump_mask = shader.inputs.new(NODE_SOCKET_COLOR, 'Bump Mask')
    output_microbump1 = shader.inputs.new(NODE_SOCKET_COLOR, 'MicroBump 1')
    output_microbump1.default_value = (NORMAL_COLOR)
    output_microbump2 = shader.inputs.new(NODE_SOCKET_COLOR, 'MicroBump 2')
    output_microbump2.default_value = (NORMAL_COLOR)
    output_environment = shader.inputs.new(NODE_SOCKET_COLOR, 'Environment')
    output_alpha = shader.inputs.new(NODE_SOCKET_FLOAT_FACTOR, 'Alpha')
    output_alpha.min_value = 0
    output_alpha.max_value = 1
    output_alpha.default_value = 1

    # Group outputs
    shader.outputs.new(NODE_SOCKET_SHADER, 'Shader')

    principled = shader.nodes.new(PRINCIPLED_SHADER_NODE)

    # Diffuse and Lightmap
    mix_rgb = shader.nodes.new(RGB_MIX_NODE)
    mix_rgb.location += Vector((-800, 100))
    mix_rgb.inputs[0].default_value = 1
    mix_rgb.blend_type = 'MULTIPLY'

    shader.links.new(group_input.outputs['Diffuse'], mix_rgb.inputs[1])
    shader.links.new(group_input.outputs['Lightmap'], mix_rgb.inputs[2])
    shader.links.new(mix_rgb.outputs['Color'], principled.inputs['Base Color'])

    # Specular
    bw = shader.nodes.new(RGB_TO_BW_NODE)
    bw.location += Vector((-800, -100))
    pow = shader.nodes.new(SHADER_NODE_MATH)
    pow.location += Vector((-600, -100))
    pow.inputs[1].default_value = 2
    pow.operation = 'POWER'
    inv = shader.nodes.new(INVERT_NODE)
    inv.location += Vector((-400, -100))

    shader.links.new(group_input.outputs['Specular'], bw.inputs['Color'])
    shader.links.new(bw.outputs['Val'], pow.inputs[0])
    shader.links.new(pow.outputs['Value'], inv.inputs['Color'])
    shader.links.new(inv.outputs['Color'], principled.inputs['Roughness'])

    # Alpha & Emission
    shader.links.new(group_input.outputs['Alpha'], principled.inputs['Alpha'])
    shader.links.new(group_input.outputs['Emission'], principled.inputs['Emission'])

    # Normals
    normal_invert_channel = getNodeGroup(shader, INVERT_CHANNEL_NODE)
    normal_invert_channel.location += Vector((-800, -500))
    # normal_invert_channel.inputs['R'].default_value = flags[xps_const.TANGENT_SPACE_RED]
    # normal_invert_channel.inputs['G'].default_value = flags[xps_const.TANGENT_SPACE_GREEN]
    # normal_invert_channel.inputs['B'].default_value = flags[xps_const.TANGENT_SPACE_BLUE]
    shader.links.new(group_input.outputs['Bump Map'], normal_invert_channel.inputs['Color'])

    microbump1_invert_channel = getNodeGroup(shader, INVERT_CHANNEL_NODE)
    microbump1_invert_channel.location += Vector((-800, -700))
    # microbump1_invert_channel.inputs['R'].default_value = flags[xps_const.TANGENT_SPACE_RED]
    # microbump1_invert_channel.inputs['G'].default_value = flags[xps_const.TANGENT_SPACE_GREEN]
    # microbump1_invert_channel.inputs['B'].default_value = flags[xps_const.TANGENT_SPACE_BLUE]
    shader.links.new(group_input.outputs['MicroBump 1'], microbump1_invert_channel.inputs['Color'])

    microbump2_invert_channel = getNodeGroup(shader, INVERT_CHANNEL_NODE)
    microbump2_invert_channel.location += Vector((-800, -900))
    # microbump2_invert_channel.inputs['R'].default_value = flags[xps_const.TANGENT_SPACE_RED]
    # microbump2_invert_channel.inputs['G'].default_value = flags[xps_const.TANGENT_SPACE_GREEN]
    # microbump2_invert_channel.inputs['B'].default_value = flags[xps_const.TANGENT_SPACE_BLUE]
    shader.links.new(group_input.outputs['MicroBump 2'], microbump2_invert_channel.inputs['Color'])

    normal_mask = getNodeGroup(shader, NORMAL_MASK_NODE)
    normal_mask.location += Vector((-600, -600))
    shader.links.new(group_input.outputs['Bump Mask'], normal_mask.inputs['Mask'])

    normal_mix = getNodeGroup(shader, MIX_NORMAL_NODE)
    normal_mix.location += Vector((-400, -500))

    normal_map = shader.nodes.new(NORMAL_MAP_NODE)
    normal_map.location += Vector((-200, -500))

    shader.links.new(microbump1_invert_channel.outputs['Color'], normal_mask.inputs['Normal1'])
    shader.links.new(microbump2_invert_channel.outputs['Color'], normal_mask.inputs['Normal2'])

    shader.links.new(normal_mask.outputs['Normal'], normal_mix.inputs['Detail'])
    shader.links.new(normal_invert_channel.outputs['Color'], normal_mix.inputs['Main'])
    shader.links.new(normal_mix.outputs['Color'], normal_map.inputs['Color'])
    shader.links.new(normal_map.outputs['Normal'], principled.inputs['Normal'])

    # Emission
    emission_shader = shader.nodes.new(BSDF_EMISSION_NODE)
    emission_shader.location += Vector((100, 200))
    shader_add = shader.nodes.new(SHADER_ADD_NODE)
    shader_add.location += Vector((300, 100))

    shader.links.new(group_input.outputs['Environment'], emission_shader.inputs['Color'])
    shader.links.new(emission_shader.outputs['Emission'], shader_add.inputs[0])
    shader.links.new(principled.outputs['BSDF'], shader_add.inputs[1])
    shader.links.new(shader_add.outputs['Shader'], group_output.inputs[0])

    return shader


def remove_group():
    bpy.data.node_groups.remove(bpy.data.node_groups[0])


def test():
    bpy.data.node_groups[0]
    bpy.data.node_groups.remove('MMDBasicShader')
    bpy.data.node_groups.remove(bpy.data.node_groups[0])


def run():
    material = bpy.context.active_object.active_material
    mmd_basic_shader_grp = xps_shader_group()
    shader = material.node_tree.nodes.new(NODE_GROUP)
    shader.node_tree = mmd_basic_shader_grp
    shader.width = 200

def acti():
    bpy.context.active_object.active_material.node_tree.nodes.active
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.nodes.active






#    NodeSocketVector
#    NodeSocketIntFactor
#    NodeSocketInt
#    NodeSocketFloatUnsigned
#    NodeSocketVectorAcceleration
#    NodeSocketIntUnsigned
#    NodeSocketVectorVelocity
#    NodeSocketFloatAngle
#    NodeSocketVirtual
#    NodeSocketVectorXYZ
#    NodeSocketVectorDirection
#    NodeSocketBool
#    NodeSocketIntPercentage
#    NodeSocketColor
#    NodeSocketFloatTime
#    NodeSocketVectorTranslation
#    NodeSocketFloatFactor
#    NodeSocketFloatPercentage
#    NodeSocketString
#    NodeSocketShader
#    NodeSocketFloat
#    NodeSocketVectorEuler

def sockets():
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketBool', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketColor', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketFloat', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketFloatAngle', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketFloatFactor', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketFloatPercentage', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketFloatTime', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketFloatUnsigned', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketInt', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketIntFactor', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketIntPercentage', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketIntUnsigned', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketShader', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketString', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVector', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVectorAcceleration', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVectorDirection', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVectorEuler', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVectorTranslation', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVectorVelocity', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVectorXYZ', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketVirtual', 'z')
    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.outputs.new('NodeSocketStandard', 'z')


    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.nodes.active.inputs.new('NodeSocketVector', 'z')

    bpy.context.active_object.active_material.node_tree.nodes.active.node_tree.inputs.new('NodeSocketBool', 'z')
