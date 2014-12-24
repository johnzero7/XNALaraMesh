# -*- coding: utf-8 -*-

class RenderType():
    def __init__(self):
        self.renderGroupNum = None
        self.meshName = None
        self.specularity = None
        self.bump1rep = None
        self.bump2rep = None
        self.val4 = None

class RenderGroup:
    def __init__(self, renderType):
        self.renderType = renderType
        self.renderGroupNum = renderType.renderGroupNum
        self.rgShadding = None
        self.rgAlpha = None
        self.rgPosable = None
        self.rgSpecular = None
        self.rgBump1Rep = None
        self.rgBump2Rep = None
        self.rgTexCount = None
        self.rgTexType = None

        if self.renderGroupNum == 1:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType=['diffuse','lightmap','bumpmap','mask','bump1','bump2']
        if self.renderGroupNum == 2:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','lightmap','bumpmap']
        if self.renderGroupNum == 3:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','lightmap']
        if self.renderGroupNum == 4:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','bumpmap']
        if self.renderGroupNum == 5:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 6:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','bumpmap']
        if self.renderGroupNum == 7:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 8:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','lightmap','bumpmap']
        if self.renderGroupNum == 9:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','lightmap']
        if self.renderGroupNum == 10:
            self.rgShadding = 'No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 11:
            self.rgShadding = 'Vertex'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','bumpmap']
        if self.renderGroupNum == 12:
            self.rgShadding = 'Vertex'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','bumpmap']
        if self.renderGroupNum == 13:
            self.rgShadding = 'No'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 14:
            self.rgShadding = 'No'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','bumpmap']
        if self.renderGroupNum == 15:
            self.rgShadding = 'No'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','bumpmap']
        if self.renderGroupNum == 16:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 17:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','lightmap']
        if self.renderGroupNum == 18:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 19:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = False
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 2
            self.rgTexType=['diffuse','lightmap']
        if self.renderGroupNum == 20:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType=['diffuse','lightmap','bumpmap','mask','bump1','bump2']
        if self.renderGroupNum == 21:
            self.rgShadding = 'No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'No'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 22:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 7
            self.rgTexType=['diffuse','lightmap','bumpmap','mask','bump1','bump2','specular']
        if self.renderGroupNum == 23:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 7
            self.rgTexType=['diffuse','lightmap','bumpmap','mask','bump1','bump2','specular']
        if self.renderGroupNum == 24:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType=['diffuse','lightmap','bumpmap','specular']
        if self.renderGroupNum == 25:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType=['diffuse','lightmap','bumpmap','specular']
        if self.renderGroupNum == 26:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','bumpmap','enviroment']
        if self.renderGroupNum == 27:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','bumpmap','enviroment']
        if self.renderGroupNum == 28:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType=['diffuse','bumpmap','mask','bump1','bump2','enviroment']
        if self.renderGroupNum == 29:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = True
            self.rgTexCount = 6
            self.rgTexType=['diffuse','bumpmap','mask','bump1','bump2','enviroment']
        if self.renderGroupNum == 30:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','bumpmap','emission']
        if self.renderGroupNum == 31:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','bumpmap','emission']
        if self.renderGroupNum == 32:
            self.rgShadding = 'Yes'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
        if self.renderGroupNum == 33:
            self.rgShadding = 'Yes'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes'
            self.rgBump1Rep = False
            self.rgBump2Rep = False
            self.rgTexCount = 1
            self.rgTexType=['diffuse']
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
            self.rgTexType=['diffuse','bumpmap','emission_mini_map']
        if self.renderGroupNum == 37:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 3
            self.rgTexType=['diffuse','bumpmap','emission_mini_map']
        if self.renderGroupNum == 38:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = False
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType=['diffuse','bumpmap','specular','emission']
        if self.renderGroupNum == 39:
            self.rgShadding = 'Yes/No'
            self.rgAlpha = True
            self.rgPosable = True
            self.rgSpecular = 'Yes intensity'
            self.rgBump1Rep = True
            self.rgBump2Rep = False
            self.rgTexCount = 4
            self.rgTexType=['diffuse','bumpmap','specular','emission']


#class TextureType(Enum):
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

        specular_factor = renderType.specularity
        
        if not specular_factor:
            specular_factor = 1
        bump1Rep = renderType.bump1rep
        if not bump1Rep:
            bump1Rep = 1
        bump2Rep = renderType.bump2rep
        if not bump2Rep:
            bump2Rep = 1

        textureSlot = materialData.texture_slots[texIndex]
        texture = textureSlot.texture

        materialData.use_transparency = texAlpha
        materialData.specular_intensity = 0
        
        texType = None
        if texIndex < len(renderGroup.rgTexType):
            texType = renderGroup.rgTexType[texIndex]

        if texType == 'diffuse':
            textureSlot.use = True
            textureSlot.blend_type = 'MULTIPLY'
            texture.image.use_alpha = texAlpha
            textureSlot.use_map_alpha = texAlpha
            textureSlot.use_map_diffuse = True
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
            #textureSlot.use_rgb_to_intensity = True
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_specular = True
            textureSlot.specular_factor = specular_factor
            textureSlot.use_map_color_spec = True
        if texType == 'enviroment':
            textureSlot.use = True
            texture.image.use_alpha = texAlpha
            textureSlot.blend_type = 'MIX'
            textureSlot.use_map_diffuse = True
            textureSlot.diffuse_color_factor = specular_factor
            textureSlot.use_map_color_diffuse = True
            textureSlot.use_map_alpha = False
            textureSlot.use_map_emit = True

            textureSlot.texture_coords = 'REFLECTION'

            #textureSlot.use_rgb_to_intensity = True
        if texType == 'mask':
            textureSlot.use = False
        if texType == 'bump1':
            useTexture = bool(renderType.bump1rep)
            textureSlot.use = useTexture
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_normal = True
            textureSlot.normal_factor = 1.0
            textureSlot.normal_map_space = 'TANGENT'
            textureSlot.scale = (bump1Rep, bump1Rep, 1)
            texture.use_normal_map = True
            texture.image.use_alpha = False
        if texType == 'bump2':
            useTexture = bool(renderType.bump2rep)
            textureSlot.use = useTexture
            textureSlot.use_map_color_diffuse = False
            textureSlot.use_map_alpha = False
            textureSlot.use_map_normal = True
            textureSlot.normal_factor = 1.0
            textureSlot.normal_map_space = 'TANGENT'
            textureSlot.scale = (bump2Rep, bump2Rep, 1)
            texture.use_normal_map = True
            texture.image.use_alpha = False
        if texType == 'emission':
            textureSlot.use = True
        if texType == 'emission_mini_map':
            textureSlot.use = True



#'diffuse','lightmap','bumpmap','mask','bump1','bump2','specular','emission','enviroment','emission_mini_map'

if __name__ == "__main__":

    xx = RenderGroup(1)
    print(xx.__dict__)
    print(xx.rgTexType)
