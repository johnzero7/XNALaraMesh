# -*- coding: utf-8 -*-

from XNALaraMesh import import_xnalara_model
from XNALaraMesh import export_xnalara_model
from XNALaraMesh import import_xnalara_pose
from XNALaraMesh import export_xnalara_pose

import bpy
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty

uv_x_displace = 0
uv_y_displace = 1

class Import_Xps_Model_Op(bpy.types.Operator, ImportHelper):
    '''Load an XNALara model File'''
    bl_idname = "xps_tools.import_model"
    bl_label = "Import XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = ".mesh";

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath = bpy.props.StringProperty(
            name="File Path",
            description="Filepath used for importing the file",
            maxlen= 1024,
            default= "",
            )
    #filter File Extension
    filter_glob = bpy.props.StringProperty(
            default="*.mesh.ascii;*.mesh;*.xps",
            options={'HIDDEN'},
            )

#    removeUnusedBones = bpy.props.BoolProperty(
#            name="Remove Unused Bones?",
#            description="Remove unused bones from the armature upon import?",
#            default=False,
#            )

#    combineMeshes = bpy.props.BoolProperty(
#            name="Combine Meshes?",
#            description="Combine all meshes into a single object?",
#            default=False,
#            )
    removeUnusedBones = True
    combineMeshes = True
    
    #my_float = bpy.props.FloatProperty(name="Some Floating Point")
    #my_bool = bpy.props.BoolProperty(name="Toggle Option")
    #my_string = bpy.props.StringProperty(name="String Value")
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

    def execute(self, context):
        import_xnalara_model.getInputFilename(
            self.filepath,
            self.removeUnusedBones,
            self.combineMeshes,
            self.uvDisplX,
            self.uvDisplY,
            self.impDefPose,
            )
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label('UV Displace:')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        layout.prop(self, "impDefPose")


class Export_Xps_Model_Op(bpy.types.Operator, ExportHelper):
    '''Save an XNALara model File'''
    bl_idname = "xps_tools.export_model"
    bl_label = "Export XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    #filename_ext = '.mesh';
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
    filepath = bpy.props.StringProperty(
            name="File Path",
            description="Filepath used for exporting the file",
            maxlen= 1024,
            default= "",
            )
    #filter File Extension
    filter_glob = bpy.props.StringProperty(
            default="*.mesh.ascii;*.mesh;*.xps",
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

    def execute(self, context):
        export_xnalara_model.getOutputFilename(
            self.filepath,
            self.uvDisplX,
            self.uvDisplY,
            True,
            self.expDefPose,
            self.protectMod
            )
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "filename_ext")

        isBinary = self.filename_ext in ('.mesh','.xps')
        if (isBinary):
            layout.prop(self, "protectMod")

        col = layout.column(align=True)
        col.label('UV Displace:')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        layout.prop(self, "expDefPose")

class Import_Xps_Pose_Op(bpy.types.Operator, ImportHelper):
    '''Load an XNALara pose File'''
    bl_idname = "xps_tools.import_pose"
    bl_label = "Import XNALara/XPS Pose"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.pose';

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath = bpy.props.StringProperty(
            name="File Path",
            description="Filepath used for importing the file",
            maxlen= 1024,
            default= "",
            )

    #filter File Extension
    filter_glob = bpy.props.StringProperty(
            default="*.pose",
            options={'HIDDEN'},
            )

    def execute(self, context):
        import_xnalara_pose.getInputFilename(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


class Export_Xps_Pose_Op(bpy.types.Operator, ExportHelper):
    '''Save an XNALara pose File'''
    bl_idname = "xps_tools.export_pose"
    bl_label = "Export XNALara/XPS Pose"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = '.pose';

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath = bpy.props.StringProperty(
            name="File Path",
            description="Filepath used for exporting the file",
            maxlen= 1024,
            default= "",
            )
    #filter File Extension
    filter_glob = bpy.props.StringProperty(
            default="*.pose",
            options={'HIDDEN'},
            )

    def execute(self, context):
        export_xnalara_pose.getOutputFilename(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


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
    bpy.utils.register_class(Import_Xps_Model_Op)
    bpy.utils.register_class(Export_Xps_Model_Op)
    bpy.utils.register_class(Import_Xps_Pose_Op)
    bpy.utils.register_class(Export_Xps_Pose_Op)
    bpy.types.INFO_MT_file_import.append(menu_func_model_import)
    bpy.types.INFO_MT_file_export.append(menu_func_model_export)
    bpy.types.INFO_MT_file_import.append(menu_func_pose_import)
    bpy.types.INFO_MT_file_export.append(menu_func_pose_export)

    
def unregister():
    bpy.types.INFO_MT_file_import.remove(menu_func_model_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_model_export)
    bpy.types.INFO_MT_file_import.remove(menu_func_pose_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_pose_export)
    bpy.utils.unregister_class(Import_Xps_Model_Op)
    bpy.utils.unregister_class(Export_Xps_Model_Op)
    bpy.utils.unregister_class(Import_Xps_Pose_Op)
    bpy.utils.unregister_class(Export_Xps_Pose_Op)


if __name__ == "__main__":
    register()



