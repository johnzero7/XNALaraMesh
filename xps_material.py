# -*- coding: utf-8 -*-
# <pep8 compliant>

import math

from . import ascii_ops
import bpy


class RenderType():

    def __init__(self):
        self.renderGroupNum = None
        self.meshName = None
        self.specularity = None
        self.texRepeater1 = None
        self.texRepeater2 = None
        self.val4 = None


class RenderGroup:

    def __init__(self, renderType):
        self.renderType = renderType
        self.renderGroupNum = renderType.renderGroupNum
        self.rgShadding = 'Yes'
        self.rgAlpha = False
        self.rgPosable = True
        self.rgSpecular = 'Yes'
        self.rgBump1Rep = True
        self.rgBump2Rep = True
        self.rgSpec1Rep = False
        self.rgTexCount = 6
        self.rgTexType = ['diffuse', 'mask', 'mask', 'mask', 'mask', 'mask']

        if self.renderGroupNum == 1:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                'diffuse',
                'lightmap',
                'bumpmap',
                'mask',
                'bump1',
                'bump2']
        if self.renderGroupNum == 2:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'lightmap', 'bumpmap']
        if self.renderGroupNum == 3:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'lightmap']
        if self.renderGroupNum == 4:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'bumpmap']
        if self.renderGroupNum == 5:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 6:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'bumpmap']
        if self.renderGroupNum == 7:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 8:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'lightmap', 'bumpmap']
        if self.renderGroupNum == 9:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'lightmap']
        if self.renderGroupNum == 10:
            self.rgShadding = False
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 11:
            self.rgShadding = 'Vertex'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'bumpmap']
        if self.renderGroupNum == 12:
            self.rgShadding = 'Vertex'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'bumpmap']
        if self.renderGroupNum == 13:
            self.rgShadding = False
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 14:
            self.rgShadding = False
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'bumpmap']
        if self.renderGroupNum == 15:
            self.rgShadding = False
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'bumpmap']
        if self.renderGroupNum == 16:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 17:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'lightmap']
        if self.renderGroupNum == 18:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 19:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = ['diffuse', 'lightmap']
        if self.renderGroupNum == 20:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                'diffuse',
                'lightmap',
                'bumpmap',
                'mask',
                'bump1',
                'bump2']
        if self.renderGroupNum == 21:
            self.rgShadding = False
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 22:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 7
            self.rgTexType = [
                'diffuse',
                'lightmap',
                'bumpmap',
                'mask',
                'bump1',
                'bump2',
                'specular']
        if self.renderGroupNum == 23:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 7
            self.rgTexType = [
                'diffuse',
                'lightmap',
                'bumpmap',
                'mask',
                'bump1',
                'bump2',
                'specular']
        if self.renderGroupNum == 24:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = ['diffuse', 'lightmap', 'bumpmap', 'specular']
        if self.renderGroupNum == 25:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = ['diffuse', 'lightmap', 'bumpmap', 'specular']
        if self.renderGroupNum == 26:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = ['diffuse', 'bumpmap', 'enviroment', 'mask']
        if self.renderGroupNum == 27:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = ['diffuse', 'bumpmap', 'enviroment', 'mask']
        if self.renderGroupNum == 28:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                'diffuse',
                'bumpmap',
                'mask',
                'bump1',
                'bump2',
                'enviroment']
        if self.renderGroupNum == 29:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                'diffuse',
                'bumpmap',
                'mask',
                'bump1',
                'bump2',
                'enviroment']
        if self.renderGroupNum == 30:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'emission']
        if self.renderGroupNum == 31:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'emission']
        if self.renderGroupNum == 32:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 33:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = ['diffuse']
        if self.renderGroupNum == 34:
            pass
        if self.renderGroupNum == 35:
            pass
        if self.renderGroupNum == 36:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'emission_mini_map']
        if self.renderGroupNum == 37:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'emission_mini_map']
        if self.renderGroupNum == 38:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = ['diffuse', 'bumpmap', 'specular', 'emission']
        if self.renderGroupNum == 39:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = ['diffuse', 'bumpmap', 'specular', 'emission']
        if self.renderGroupNum == 40:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'specular']
        if self.renderGroupNum == 41:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'specular']
        if self.renderGroupNum == 42:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgSpec1Rep = True
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'specular']
        if self.renderGroupNum == 43:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgSpec1Rep = True
            self.rgTexCount = 3
            self.rgTexType = ['diffuse', 'bumpmap', 'specular']


def makeRenderType(meshFullName):
    mat = meshFullName.split("_")
    maxLen = 8
    # Complete the array with None
    mat = mat + [None] * (maxLen - len(mat))

    renderType = RenderType()

    renderGroupNum = 5
    meshName = 'mesh'
    specularity = 1
    texRepeater1 = 0
    texRepeater2 = 0

    renderGroupFloat = ascii_ops.getFloat(mat[0])
    # meshName = mat[1]
    # specularityFloat = ascii_ops.getFloat(mat[2])
    # texRepeater1Float = ascii_ops.getFloat(mat[3])
    # texRepeater2Float = ascii_ops.getFloat(mat[4])

    if math.isnan(renderGroupFloat):
        meshName = mat[0]
        specularityFloat = ascii_ops.getFloat(mat[1])
        texRepeater1Float = ascii_ops.getFloat(mat[2])
        texRepeater2Float = ascii_ops.getFloat(mat[3])
    else:
        renderGroupNum = int(renderGroupFloat)
        meshName = mat[1]
        specularityFloat = ascii_ops.getFloat(mat[2])
        texRepeater1Float = ascii_ops.getFloat(mat[3])
        texRepeater2Float = ascii_ops.getFloat(mat[4])

    if specularityFloat and not math.isnan(specularityFloat):
        specularity = specularityFloat
    if texRepeater1Float and not math.isnan(texRepeater1Float):
        texRepeater1 = texRepeater1Float
    if texRepeater2Float and not math.isnan(texRepeater2Float):
        texRepeater2 = texRepeater2Float
    if mat[5]:
        renderType.val4 = mat[5]

    renderType.renderGroupNum = renderGroupNum
    renderType.meshName = meshName
    renderType.specularity = specularity
    renderType.texRepeater1 = texRepeater1
    renderType.texRepeater2 = texRepeater2

    return renderType


def makeRenderTypeName(renderType):
    nameList = []

    if renderType.renderGroupNum:
        nameList.append(str(renderType.renderGroupNum))
    if renderType.meshName is not None:
        nameList.append(renderType.meshName)
    if renderType.specularity is not None:
        nameList.append(str(renderType.specularity))
    if renderType.texRepeater1 is not None:
        nameList.append(str(renderType.texRepeater1))
    if renderType.texRepeater2 is not None:
        nameList.append(str(renderType.texRepeater2))
    if renderType.val4 is not None:
        nameList.append(str(renderType.val4))

    name = "_".join(nameList)
    return name

# class TextureType(Enum):
#    diffuse = 1
#    lightmap = 2
#    bumpmap = 3
#    specular = 4
#    enviroment = 5
#    mask = 6
#    bump1 = 7
#    bump2 = 8
#    emission = 9
#    emission_mini_map = 10


def textureSlot(renderGroup, texIndex, materialData):

    renderType = renderGroup.renderType
    if renderType.renderGroupNum:
        texAlpha = renderGroup.rgAlpha
        shadding = not bool(renderGroup.rgShadding)

        specular_factor = renderType.specularity

        if not specular_factor:
            specular_factor = 1
        texRepeater1 = renderType.texRepeater1
        if not texRepeater1:
            texRepeater1 = 1
        texRepeater2 = renderType.texRepeater2
        if not texRepeater2:
            texRepeater2 = 1

        # print('SPEC', specular_factor)
        # print('TEXREP1', texRepeater1)
        # print('TEXREP2', texRepeater2)

        textureSlot = materialData.texture_slots[texIndex]
        texture = textureSlot.texture

        materialData.use_transparency = texAlpha
        if texAlpha:
            materialData.alpha = 0
        materialData.specular_intensity = 0

        texType = None
        if texIndex < len(renderGroup.rgTexType):
            texType = renderGroup.rgTexType[texIndex]

        if texType == 'diffuse':
            textureSlot.use = True
            textureSlot.blend_type = 'MIX'
            texture.image.use_alpha = texAlpha
            # textureSlot.use_map_alpha = texAlpha
            textureSlot.use_map_alpha = True
            textureSlot.use_map_diffuse = False
            textureSlot.use_map_color_diffuse = True
            materialData.use_shadeless = shadding
        if texType == 'lightmap':
            textureSlot.use = True
            textureSlot.blend_type = 'MULTIPLY'
            textureSlot.use_map_color_diffuse = True
            texture.image.use_alpha = texAlpha
            textureSlot.use_map_alpha = texAlpha
        if texType == 'bumpmap':
            textureSlot.use = True
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_normal = True
            textureSlot.normal_factor = 1.0
            textureSlot.normal_map_space = 'TANGENT'
            texture.use_normal_map = True
            texture.image.use_alpha = False
        if texType == 'specular':
            textureSlot.use = True
            # textureSlot.use_rgb_to_intensity = True
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_specular = True
            textureSlot.specular_factor = specular_factor
            textureSlot.use_map_color_spec = True
            if renderGroup.rgSpec1Rep:
                scaleTex(textureSlot, texRepeater1)
        if texType == 'enviroment':
            textureSlot.use = True
            texture.image.use_alpha = texAlpha
            textureSlot.blend_type = 'MIX'
            textureSlot.use_map_diffuse = False
            textureSlot.diffuse_color_factor = specular_factor
            textureSlot.use_map_color_diffuse = True
            textureSlot.use_map_alpha = False
            textureSlot.use_map_emit = True
            textureSlot.emit_factor = specular_factor
            textureSlot.texture_coords = 'REFLECTION'
            # textureSlot.use_rgb_to_intensity = True
        if texType == 'mask':
            textureSlot.use = False
            textureSlot.use_map_alpha = False
        if texType == 'bump1':
            texRepeater = None
            if renderGroup.renderGroupNum in (28,29):
                texRepeater = renderType.texRepeater2
            else:
                texRepeater = renderType.texRepeater1
            useTexture = bool(texRepeater)
            textureSlot.use = useTexture
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_normal = True
            textureSlot.normal_factor = 1.0
            textureSlot.normal_map_space = 'TANGENT'
            if renderGroup.rgBump1Rep:
                scaleTex(textureSlot, texRepeater)
            texture.use_normal_map = True
            texture.image.use_alpha = False
        if texType == 'bump2':
            texRepeater = renderType.texRepeater2
            useTexture = bool(texRepeater)
            textureSlot.use = useTexture
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_normal = True
            textureSlot.normal_factor = 1.0
            textureSlot.normal_map_space = 'TANGENT'
            if renderGroup.rgBump2Rep:
                scaleTex(textureSlot, texRepeater)
            texture.use_normal_map = True
            texture.image.use_alpha = False
        if texType == 'emission':
            textureSlot.use = True
            textureSlot.use_map_emit = True
            textureSlot.emit_factor = 1
            textureSlot.blend_type = 'ADD'
        if texType == 'emission_mini_map':
            textureSlot.use = True
            textureSlot.use_map_emit = True
            textureSlot.emit_factor = 1
            textureSlot.blend_type = 'MIX'
            textureSlot.scale = (texRepeater1, texRepeater1, 1)


def texScaleOffset(scale):
    offset = (scale / 2.0) - ((int(scale)-1)//2) - .5
    return offset


def scaleTex(textureSlot, texScale):
    textureSlot.scale = (texScale, texScale, 1)
    offset = texScaleOffset(texScale)
    textureSlot.offset = (offset, -offset, 1)

# All available texture types are:
# 'diffuse','lightmap','bumpmap','mask','bump1','bump2','specular','emission','enviroment','emission_mini_map'


if __name__ == "__main__":
    rt = RenderType()
    xx = RenderGroup(rt)
    print(xx.__dict__)
    print(xx.rgTexType)
