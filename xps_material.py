# <pep8 compliant>

import math

from . import ascii_ops
from enum import Enum


# All available texture types:
class TextureType(Enum):
    DIFFUSE = 'diffuse'                     # 1
    LIGHT = 'lightmap'                      # 2
    BUMP = 'bump'                           # 3
    MASK = 'mask'                           # 4
    BUMP1 = 'bump1'                         # 5
    BUMP2 = 'bump2'                         # 6
    SPECULAR = 'specular'                   # 7
    ENVIRONMENT = 'environment'             # 8
    EMISSION = 'emission'                   # 9
    EMISSION_MINI = 'emission_mini'         # 10


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
        self.rgTexType = [
            TextureType.DIFFUSE,
            TextureType.MASK,
            TextureType.MASK,
            TextureType.MASK,
            TextureType.MASK,
            TextureType.MASK]

        if self.renderGroupNum == 1:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.LIGHT,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.BUMP1,
                TextureType.BUMP2]
        if self.renderGroupNum == 2:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.LIGHT, TextureType.BUMP]
        if self.renderGroupNum == 3:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.LIGHT]
        if self.renderGroupNum == 4:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP]
        if self.renderGroupNum == 5:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 6:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP]
        if self.renderGroupNum == 7:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 8:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.LIGHT, TextureType.BUMP]
        if self.renderGroupNum == 9:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.LIGHT]
        if self.renderGroupNum == 10:
            self.rgShadding = False
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 11:
            self.rgShadding = 'Vertex'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP]
        if self.renderGroupNum == 12:
            self.rgShadding = 'Vertex'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP]
        if self.renderGroupNum == 13:
            self.rgShadding = False
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 14:
            self.rgShadding = False
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP]
        if self.renderGroupNum == 15:
            self.rgShadding = False
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP]
        if self.renderGroupNum == 16:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 17:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.LIGHT]
        if self.renderGroupNum == 18:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 19:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType = [TextureType.DIFFUSE, TextureType.LIGHT]
        if self.renderGroupNum == 20:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.LIGHT,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.BUMP1,
                TextureType.BUMP2]
        if self.renderGroupNum == 21:
            self.rgShadding = False
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 22:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 7
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.LIGHT,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.BUMP1,
                TextureType.BUMP2,
                TextureType.SPECULAR]
        if self.renderGroupNum == 23:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 7
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.LIGHT,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.BUMP1,
                TextureType.BUMP2,
                TextureType.SPECULAR]
        if self.renderGroupNum == 24:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.LIGHT,
                TextureType.BUMP,
                TextureType.SPECULAR]
        if self.renderGroupNum == 25:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.LIGHT,
                TextureType.BUMP,
                TextureType.SPECULAR]
        if self.renderGroupNum == 26:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.ENVIRONMENT,
                TextureType.MASK]
        if self.renderGroupNum == 27:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.ENVIRONMENT,
                TextureType.MASK]
        if self.renderGroupNum == 28:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.BUMP1,
                TextureType.BUMP2,
                TextureType.ENVIRONMENT]
        if self.renderGroupNum == 29:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.BUMP1,
                TextureType.BUMP2,
                TextureType.ENVIRONMENT]
        if self.renderGroupNum == 30:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.EMISSION]
        if self.renderGroupNum == 31:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.EMISSION]
        if self.renderGroupNum == 32:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 33:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType = [TextureType.DIFFUSE]
        if self.renderGroupNum == 34:
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.SPECULAR]
        if self.renderGroupNum == 35:
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.MASK,
                TextureType.SPECULAR]
        if self.renderGroupNum == 36:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.EMISSION_MINI]
        if self.renderGroupNum == 37:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.EMISSION_MINI]
        if self.renderGroupNum == 38:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.SPECULAR,
                TextureType.EMISSION]
        if self.renderGroupNum == 39:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType = [
                TextureType.DIFFUSE,
                TextureType.BUMP,
                TextureType.SPECULAR,
                TextureType.EMISSION]
        if self.renderGroupNum == 40:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.SPECULAR]
        if self.renderGroupNum == 41:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.SPECULAR]
        if self.renderGroupNum == 42:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgSpec1Rep = True
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.SPECULAR]
        if self.renderGroupNum == 43:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgSpec1Rep = True
            self.rgTexCount = 3
            self.rgTexType = [TextureType.DIFFUSE, TextureType.BUMP, TextureType.SPECULAR]


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


def texScaleOffset(scale):
    offset = (scale / 2.0) - ((int(scale)-1)//2) - .5
    return offset


def scaleTex(textureSlot, texScale):
    textureSlot.scale = (texScale, texScale, 1)
    offset = texScaleOffset(texScale)
    textureSlot.offset = (offset, -offset, 1)


if __name__ == "__main__":
    rt = RenderType()
    xx = RenderGroup(rt)
    print(xx.__dict__)
    print(xx.rgTexType)
