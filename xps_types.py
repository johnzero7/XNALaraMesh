# <pep8 compliant>


class XpsBone:

    def __init__(self, id, name, co, parentId):
        self.id = id
        self.name = name
        self.co = co
        self.parentId = parentId


class XpsBonePose:

    def __init__(self, boneName, coordDelta, rotDelta, scale):
        self.boneName = boneName
        self.coordDelta = coordDelta
        self.rotDelta = rotDelta
        self.scale = scale


class XpsMesh:

    def __init__(self, name, textures, vertices, faces, uvCount):
        self.name = name
        self.textures = textures
        self.vertices = vertices
        self.faces = faces
        self.uvCount = uvCount


class BoneWeight:

    def __init__(self, id, weight):
        self.id = id
        self.weight = weight


class XpsVertex:

    def __init__(self, id, co, norm, vColor, uv, boneWeights):
        self.id = id
        self.co = co
        self.norm = norm
        self.vColor = vColor
        self.uv = uv
        self.boneWeights = boneWeights
        self.merged = False

    def __copy__(self):
        return XpsVertex(
                self.id,
                self.co[:],
                self.norm[:],
                self.vColor[:],
                self.uv[:],
                self.boneWeights
                )


class XpsTexture:

    def __init__(self, id, file, uvLayer):
        self.id = id
        self.file = file
        self.uvLayer = uvLayer


class XpsData:

    def __init__(self, header='', bones=[], meshes=[]):
        self.header = header
        self.bones = bones
        self.meshes = meshes


class XpsHeader:

    def __init__(
            self,
            magic_number=323232,
            version_mayor=2,
            version_minor=15,
            xna_aral='XNAaraL',
            settingsLen=275,
            machine='',
            user='',
            files='',
            settings='',
            pose=''):
        self.magic_number = magic_number
        self.version_mayor = version_mayor
        self.version_minor = version_minor
        self.xna_aral = xna_aral
        self.settingsLen = settingsLen
        self.machine = machine
        self.user = user
        self.files = files
        self.settings = settings
        self.pose = pose


class XpsImportSettings:

    def __init__(
            self,
            filename,
            uvDisplX,
            uvDisplY,
            importDefaultPose,
            joinMeshRips,
            joinMeshParts,
            markSeams,
            vColors,
            connectBones,
            autoIk,
            importNormals):
        self.filename = filename
        self.uvDisplX = uvDisplX
        self.uvDisplY = uvDisplY
        self.importDefaultPose = importDefaultPose
        self.joinMeshRips = joinMeshRips
        self.joinMeshParts = joinMeshParts
        self.markSeams = markSeams
        self.vColors = vColors
        self.connectBones = connectBones
        self.autoIk = autoIk
        self.importNormals = importNormals


class XpsExportSettings:

    def __init__(
            self,
            filename,
            uvDisplX,
            uvDisplY,
            exportOnlySelected,
            expDefPose,
            preserveSeams,
            vColors,
            exportNormals):
        self.filename = filename
        self.uvDisplX = uvDisplX
        self.uvDisplY = uvDisplY
        self.exportOnlySelected = exportOnlySelected
        self.expDefPose = expDefPose
        self.preserveSeams = preserveSeams
        self.vColors = vColors
        self.exportNormals = exportNormals
