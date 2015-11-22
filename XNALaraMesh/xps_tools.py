# -*- coding: utf-8 -*-

from XNALaraMesh import export_xnalara_model
from XNALaraMesh import export_xnalara_pose
from XNALaraMesh import import_xnalara_model
from XNALaraMesh import import_xnalara_pose
from XNALaraMesh import xps_types
import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper
from bpy_extras.io_utils import ImportHelper


uv_x_displace = 0
uv_y_displace = 0


class Import_Xps_Model_Op(bpy.types.Operator, ImportHelper):

    '''Load an XNALara model File'''
    bl_idname = "xps_tools.import_model"
    bl_label = "Import XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = ".mesh"

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob = bpy.props.StringProperty(
        default="*.ascii;*.mesh;*.xps",
        options={'HIDDEN'},
    )

    uvDisplX = bpy.props.IntProperty(
        name="X",
        description="Displace UV X axis",
        default=uv_x_displace,
    )

    uvDisplY = bpy.props.IntProperty(
        name="Y",
        description="Displace UV Y axis",
        default=uv_y_displace,
    )

    impDefPose = BoolProperty(
        name="Default Pose",
        description="Import Default Pose",
        default=False,
    )

    markSeams = BoolProperty(
        name="Mark Seams",
        description="Mark as Seams the edged merged by the addon",
        default=True,
    )

    joinMeshRips = BoolProperty(
        name="Merge Doubles by Normal",
        description="Merge vertices with the same position and normal",
        default=True,
    )

    joinMeshParts = BoolProperty(
        name="Join MeshParts",
        description="Join MeshParts (meshes that contain 'nPart!' in the name)",
        default=True,
    )

    connectBones = BoolProperty(
        name="Connect Bones",
        description="Connect Bones all bones",
        default=True,
    )

    autoIk = BoolProperty(
        name="AutoIK",
        description="Set AutoIK",
        default=True,
    )

    importNormals = BoolProperty(
        name="Import Normals",
        description="Import Custom Normals",
        default=True,
    )

    # Only needed if you want to add into a dynamic menu
    def menu_func(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        self.layout.operator(
            Import_Xps_Model_Op.bl_idname,
            text="Text Export Operator")

    @classmethod
    def poll(cls, context):
        # Always can import
        return True

    def execute(self, context):
        xpsSettings = xps_types.XpsImportSettings(
            self.filepath,
            self.uvDisplX,
            self.uvDisplY,
            self.impDefPose,
            self.joinMeshRips,
            self.joinMeshParts,
            self.markSeams and self.joinMeshRips,
            self.connectBones,
            self.autoIk,
            self.importNormals
        )
        status = import_xnalara_model.getInputFilename(xpsSettings)
        if status == '{PROTECTED}':
            # self.report({'DEBUG'}, "DEBUG Model is Mod-Protected")
            # self.report({'INFO'}, "INFO Model is Mod-Protected")
            # self.report({'OPERATOR'}, "OPERATOR Model is Mod-Protected")
            self.report({'WARNING'}, "WARNING Model is Mod-Protected")
            # self.report({'ERROR'}, "ERROR Model is Mod-Protected")
        if status == '{NONE}':
            self.report({'ERROR'}, "ERROR File Format unrecognized")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label('UV Displace')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        col = layout.column(align=True)
        col.label('Mesh')
        col.prop(self, "joinMeshParts")
        col.prop(self, "joinMeshRips")
        sub = col.row()
        sub.prop(self, "markSeams")
        col.prop(self, "importNormals")
        
        sub.enabled = self.joinMeshRips
        self.markSeams = self.joinMeshRips and self.markSeams

        col = layout.column(align=True)
        col.label('Armature')
        col.prop(self, "impDefPose")
        col.prop(self, "connectBones")
        col.prop(self, "autoIk")


class Export_Xps_Model_Op(bpy.types.Operator, ExportHelper):

    '''Save an XNALara model File'''
    bl_idname = "xps_tools.export_model"
    bl_label = "Export XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    # filename_ext = '.mesh';
    filename_ext = EnumProperty(
        name='Format',
        description='Choose Export Format',
        items=(('.mesh', 'XnaLara/XPS Binary', 'Export as XnaLara/XPS Binary'),
               ('.ascii', 'XnaLara/XPS Ascii', 'Export as XnaLara/XPS Ascii'),
               ('.xps', 'XPS Binary', 'Export as XPS Binary')),
        default='.mesh',
    )

    protectMod = BoolProperty(
        name="Protected",
        description="Prevents the model form being imported and modified",
        default=False,
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob = bpy.props.StringProperty(
        default="*.ascii;*.mesh;*.xps",
        options={'HIDDEN'},
    )

    uvDisplX = bpy.props.IntProperty(
        name="X",
        description="Displace UV X axis",
        default=uv_x_displace,
    )

    uvDisplY = bpy.props.IntProperty(
        name="Y",
        description="Displace UV Y axis",
        default=uv_y_displace,
    )

    expDefPose = BoolProperty(
        name="Default Pose",
        description="Export Default Pose",
        default=False,
    )

    exportOnlySelected = BoolProperty(
        name="Export Only Selected",
        description="Export only selected objects",
        default=True,
    )

    exportNormals = BoolProperty(
        name="Export Normals",
        description="Export Custom Normals",
        default=True,
    )

    preserveSeams = BoolProperty(
        name="Preserve Seams",
        description="Split Edges marked as seams. They are marked as seams when imported back",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'MESH'),
                None))

    def execute(self, context):
        xpsSettings = xps_types.XpsExportSettings(
            self.filepath,
            self.uvDisplX,
            self.uvDisplY,
            self.exportOnlySelected,
            self.expDefPose,
            self.protectMod,
            self.preserveSeams,
            self.exportNormals
        )
        export_xnalara_model.getOutputFilename(xpsSettings)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "filename_ext")

        isBinary = self.filename_ext in ('.mesh', '.xps')
        if (isBinary):
            layout.prop(self, "protectMod")

        col = layout.column(align=True)
        col.label('Mesh')
        col.prop(self, "preserveSeams")

        col = layout.column(align=True)
        col.label('UV Displace')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        layout.prop(self, "expDefPose")
        layout.prop(self, "exportOnlySelected")
        layout.prop(self, "exportNormals")


class Import_Xps_Pose_Op(bpy.types.Operator, ImportHelper):

    '''Load an XNALara pose File'''
    bl_idname = "xps_tools.import_pose"
    bl_label = "Import XNALara/XPS Pose"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob = bpy.props.StringProperty(
        default="*.pose",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        import_xnalara_pose.getInputFilename(self.filepath)
        return {'FINISHED'}


class Export_Xps_Pose_Op(bpy.types.Operator, ExportHelper):

    '''Save an XNALara pose File'''
    bl_idname = "xps_tools.export_pose"
    bl_label = "Export XNALara/XPS Pose"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob = bpy.props.StringProperty(
        default="*.pose",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        export_xnalara_pose.getOutputFilename(self.filepath)
        return {'FINISHED'}


class Import_Poses_To_Keyframes_Op(bpy.types.Operator, ImportHelper):

    '''Load a sequence of posese as keyframes'''
    bl_idname = "xps_tools.import_poses_to_keyframes"
    bl_label = "Import poses to keyframes"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob = bpy.props.StringProperty(
        default="*.pose",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        import_xnalara_pose.getInputPoseSequence(self.filepath)
        return {'FINISHED'}


class Export_Frames_To_Poses_Op(bpy.types.Operator, ExportHelper):

    '''Save frames as poses'''
    bl_idname = "xps_tools.export_frames_to_poses"
    bl_label = "Export frames to poses"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob = bpy.props.StringProperty(
        default="*.pose",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        export_xnalara_pose.getOutputPoseSequence(self.filepath)
        return {'FINISHED'}

class ArmatureBoneDictRename_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_dictionary_rename'
    bl_label = 'Dictionary Rename'
    bl_description = 'Use BoneDict to Rename Bones'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.txt'
    check_extension = True

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath = StringProperty(
            name="File Path",
            description="Bone Dictionary File",
            maxlen=1024,
            subtype='FILE_PATH',
            )


    # filter File Extension
    filter_glob = bpy.props.StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        armatureObj = next((obj for obj in context.selected_objects if obj.type == 'ARMATURE'), None)
        import_xnalara_model.boneDictRename(self.filepath, armatureObj)
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = 'BoneDict.txt'
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}  

    def check(self, context):
        import os
        change_ext = False
        check_extension = self.check_extension

        if check_extension is not None:
            filepath = self.filepath
            if os.path.basename(filepath):
                filepath = bpy.path.ensure_ext(filepath,
                                               self.filename_ext
                                               if check_extension
                                               else "")

                if filepath != self.filepath:
                    self.filepath = filepath
                    change_ext = True

        return (change_ext)

class ArmatureBoneDictRestore_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_dictionary_restore_name'
    bl_label = 'Dictionary Restore Names'
    bl_description = 'Use BoneDict to Restore Bone Names'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.txt'
    check_extension = True

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath = StringProperty(
            name="File Path",
            description="Bone Dictionary File",
            maxlen=1024,
            subtype='FILE_PATH',
            )


    # filter File Extension
    filter_glob = bpy.props.StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        armatureObj = next((obj for obj in context.selected_objects if obj.type == 'ARMATURE'), None)
        import_xnalara_model.boneDictRestore(self.filepath, armatureObj)
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = 'BoneDict.txt'
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}  

    def check(self, context):
        import os
        change_ext = False
        check_extension = self.check_extension

        if check_extension is not None:
            filepath = self.filepath
            if os.path.basename(filepath):
                filepath = bpy.path.ensure_ext(filepath,
                                               self.filename_ext
                                               if check_extension
                                               else "")

                if filepath != self.filepath:
                    self.filepath = filepath
                    change_ext = True

        return (change_ext)


#
# Registration
#
def menu_func_model_import(self, context):
    self.layout.operator(
        Import_Xps_Model_Op.bl_idname,
        text="XNALara/XPS Model (.ascii/.mesh/.xps)",
        icon="OUTLINER_OB_ARMATURE",
    )


def menu_func_model_export(self, context):
    self.layout.operator(
        Export_Xps_Model_Op.bl_idname,
        text="XNALara/XPS Model (.ascii/.mesh/.xps)",
        icon="OUTLINER_OB_ARMATURE",
    )


def menu_func_pose_import(self, context):
    self.layout.operator(
        Import_Xps_Pose_Op.bl_idname,
        text="XNALara/XPS Pose (.pose)",
        icon="POSE_DATA",
    )


def menu_func_pose_export(self, context):
    self.layout.operator(
        Export_Xps_Pose_Op.bl_idname,
        text="XNALara/XPS Pose (.pose)",
        icon="POSE_DATA",
    )


def register():
    bpy.types.INFO_MT_file_import.append(menu_func_model_import)
    bpy.types.INFO_MT_file_export.append(menu_func_model_export)
    bpy.types.INFO_MT_file_import.append(menu_func_pose_import)
    bpy.types.INFO_MT_file_export.append(menu_func_pose_export)


def unregister():
    bpy.types.INFO_MT_file_import.remove(menu_func_model_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_model_export)
    bpy.types.INFO_MT_file_import.remove(menu_func_pose_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_pose_export)


if __name__ == "__main__":
    register()
