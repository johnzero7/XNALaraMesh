# <pep8 compliant>

from . import export_xnalara_model
from . import export_xnalara_pose
from . import import_xnalara_model
from . import import_xnalara_pose
from . import material_creator
from . import xps_types
import bpy
import os

from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper,
        path_reference_mode,
        axis_conversion,
        _check_axis_conversion,
        )


uv_x_displace = 0
uv_y_displace = 0


class CustomExportHelper(ExportHelper):

    def check(self, context):
        import os
        change_ext = False
        change_axis = _check_axis_conversion(self)

        check_extension = self.check_extension

        if check_extension is not None:
            filepath = self.filepath
            if os.path.basename(filepath):
                filepath = bpy.path.ensure_ext(filepath,
                                               self.filename_ext
                                               if check_extension
                                               else "")

                if filepath != self.filepath:

                    head, tail = os.path.split(self.filepath)
                    filepath = os.path.splitext(tail)[0]
                    filepath = bpy.path.ensure_ext(filepath,
                                                   self.filename_ext
                                                   if check_extension
                                                   else "")
                    self.filepath = os.path.join(head, filepath)
                    change_ext = True

        return (change_ext or change_axis)


class Import_Xps_Model_Op(bpy.types.Operator, ImportHelper):
    """Load an XNALara model File."""

    bl_idname = "xps_tools.import_model"
    bl_label = "Import XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".mesh"

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
        default="*.ascii;*.mesh;*.xps",
        options={'HIDDEN'},
    )

    uvDisplX: bpy.props.IntProperty(
        name="X",
        description="Displace UV X axis",
        default=uv_x_displace,
    )

    uvDisplY: bpy.props.IntProperty(
        name="Y",
        description="Displace UV Y axis",
        default=uv_y_displace,
    )

    impDefPose: bpy.props.BoolProperty(
        name="Default Pose",
        description="Import Default Pose",
        default=False,
    )

    markSeams: bpy.props.BoolProperty(
        name="Mark Seams",
        description="Mark as Seams the edged merged by the addon",
        default=True,
    )

    vColors: bpy.props.BoolProperty(
        name="Vertex Colors",
        description="Import Vertex Colors",
        default=True,
    )

    joinMeshRips: bpy.props.BoolProperty(
        name="Merge Doubles by Normal",
        description="Merge vertices with the same position and normal",
        default=True,
    )

    joinMeshParts: bpy.props.BoolProperty(
        name="Join MeshParts",
        description="Join MeshParts (meshes that contain 'nPart!' in the name)",
        default=True,
    )

    connectBones: bpy.props.BoolProperty(
        name="Connect Bones",
        description="Connect Bones all bones",
        default=True,
    )

    autoIk: bpy.props.BoolProperty(
        name="AutoIK",
        description="Set AutoIK",
        default=True,
    )

    importNormals: bpy.props.BoolProperty(
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
            self.vColors,
            self.connectBones,
            self.autoIk,
            self.importNormals
        )
        material_creator.create_group_nodes()
        status = import_xnalara_model.getInputFilename(xpsSettings)
        if status == '{NONE}':
            # self.report({'DEBUG'}, "DEBUG File Format unrecognized")
            # self.report({'INFO'}, "INFO File Format unrecognized")
            # self.report({'OPERATOR'}, "OPERATOR File Format unrecognized")
            # self.report({'WARNING'}, "WARNING File Format unrecognized")
            # self.report({'ERROR'}, "ERROR File Format unrecognized")
            self.report({'ERROR'}, "ERROR File Format unrecognized")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='UV Displace')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        col = layout.column(align=True)
        col.label(text='Mesh')
        col.prop(self, "joinMeshParts")
        col.prop(self, "joinMeshRips")
        sub = col.row()
        sub.prop(self, "markSeams")
        col.prop(self, "importNormals")
        col.prop(self, "vColors")

        sub.enabled = self.joinMeshRips
        self.markSeams = self.joinMeshRips and self.markSeams

        col = layout.column(align=True)
        col.label(text='Armature')
        col.prop(self, "impDefPose")
        col.prop(self, "connectBones")
        col.prop(self, "autoIk")


class Export_Xps_Model_Op(bpy.types.Operator, CustomExportHelper):
    """Save an XNALara model File."""

    bl_idname = "xps_tools.export_model"
    bl_label = "Export XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER'}

    filename_ext: bpy.props.EnumProperty(
        name='Format',
        description='Choose Export Format',
        items=(
                ('.xps', 'XPS', 'Export as XPS Binary format (.xps)'),
                ('.mesh', 'MESH', 'Export as XnaLara/XPS Binary format (.mesh)'),
                ('.ascii', 'ASCII', 'Export as XnaLara/XPS Ascii format (.ascii)'),
                ),
        default='.xps',
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
        default="*.ascii;*.mesh;*.xps",
        options={'HIDDEN'},
    )

    uvDisplX: bpy.props.IntProperty(
        name="X",
        description="Displace UV X axis",
        default=uv_x_displace,
    )

    uvDisplY: bpy.props.IntProperty(
        name="Y",
        description="Displace UV Y axis",
        default=uv_y_displace,
    )

    expDefPose: bpy.props.BoolProperty(
        name="Default Pose",
        description="Export Default Pose",
        default=False,
    )

    exportOnlySelected: bpy.props.BoolProperty(
        name="Export Only Selected",
        description="Export only selected objects",
        default=True,
    )

    exportNormals: bpy.props.BoolProperty(
        name="Export Normals",
        description="Export Custom Normals",
        default=True,
    )

    preserveSeams: bpy.props.BoolProperty(
        name="Preserve Seams",
        description="Split Edges marked as seams. They are marked as seams when imported back",
        default=True,
    )

    vColors: bpy.props.BoolProperty(
        name="Vertex Colors",
        description="Export Vertex Colors",
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
            self.preserveSeams,
            self.vColors,
            self.exportNormals
        )
        export_xnalara_model.getOutputFilename(xpsSettings)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "exportOnlySelected")

        layout.label(text="File Format:")
        layout.prop(self, "filename_ext", expand=True)

        col = layout.column(align=True)
        col.label(text='Mesh')
        col.prop(self, "preserveSeams")
        col.prop(self, "exportNormals")
        col.prop(self, "vColors")

        col = layout.column(align=True)
        col.label(text='UV Displace')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        layout.prop(self, "expDefPose")


class Import_Xps_Pose_Op(bpy.types.Operator, ImportHelper):
    """Load an XNALara pose File."""

    bl_idname = "xps_tools.import_pose"
    bl_label = "Import XNALara/XPS Pose"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
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
    """Save an XNALara pose File."""

    bl_idname = "xps_tools.export_pose"
    bl_label = "Export XNALara/XPS Pose"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER'}

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
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
    """Load a sequence of posese as keyframes."""

    bl_idname = "xps_tools.import_poses_to_keyframes"
    bl_label = "Import poses to keyframes"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
        default="*.pose",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        import_xnalara_pose.getInputPoseSequence(self.filepath)
        return {'FINISHED'}


class Export_Frames_To_Poses_Op(bpy.types.Operator, CustomExportHelper):
    """Save frames as poses."""

    bl_idname = "xps_tools.export_frames_to_poses"
    bl_label = "Export frames to poses"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER'}

    filename_ext = '.pose'

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
        default="*.pose",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        export_xnalara_pose.getOutputPoseSequence(self.filepath)
        return {'FINISHED'}


class ArmatureBoneDictGenerate_Op(bpy.types.Operator):
    """Generate a BoneDict from armature."""

    bl_idname = 'xps_tools.bones_dictionary_generate'
    bl_label = 'Generate BoneDict'
    bl_description = 'Generate a BoneDict from active armature'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER'}

    filename_ext = '.txt'
    check_extension = True

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath: bpy.props.StringProperty(
            name="File Path",
            description="Bone Dictionary File",
            maxlen=1024,
            subtype='FILE_PATH',
            )

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )

    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == 'ARMATURE'

    def execute(self, context):
        armatureObj = context.active_object
        export_xnalara_model.boneDictGenerate(self.filepath, armatureObj)
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


class ArmatureBoneDictRename_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_dictionary_rename'
    bl_label = 'Dictionary Rename'
    bl_description = 'Use BoneDict to Rename Bones'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.txt'
    check_extension = True

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath: bpy.props.StringProperty(
            name="File Path",
            description="Bone Dictionary File",
            maxlen=1024,
            subtype='FILE_PATH',
            )

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
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
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.txt'
    check_extension = True

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    filepath: bpy.props.StringProperty(
            name="File Path",
            description="Bone Dictionary File",
            maxlen=1024,
            subtype='FILE_PATH',
            )

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
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


@orientation_helper(axis_forward='-Z', axis_up='Y')
class ImportXpsNgff(bpy.types.Operator, ImportHelper):
    """Load a Wavefront OBJ File."""

    bl_idname = "import_xps_ngff.obj"
    bl_label = "Import XPS NGFF"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".obj"
    filter_glob: bpy.props.StringProperty(
            default="*.obj;*.mtl;*.arl",
            options={'HIDDEN'},
            )

    use_edges: bpy.props.BoolProperty(
            name="Lines",
            description="Import lines and faces with 2 verts as edge",
            default=True,
            )
    use_smooth_groups: bpy.props.BoolProperty(
            name="Smooth Groups",
            description="Surround smooth groups by sharp edges",
            default=True,
            )

    use_split_objects: bpy.props.BoolProperty(
            name="Object",
            description="Import OBJ Objects into Blender Objects",
            default=True,
            )
    use_split_groups: bpy.props.BoolProperty(
            name="Group",
            description="Import OBJ Groups into Blender Objects",
            default=True,
            )

    use_groups_as_vgroups: bpy.props.BoolProperty(
            name="Poly Groups",
            description="Import OBJ groups as vertex groups",
            default=False,
            )

    use_image_search: bpy.props.BoolProperty(
            name="Image Search",
            description="Search subdirs for any associated images "
                        "(Warning, may be slow)",
            default=True,
            )

    split_mode: bpy.props.EnumProperty(
            name="Split",
            items=(('ON', "Split", "Split geometry, omits unused verts"),
                   ('OFF', "Keep Vert Order", "Keep vertex order from file"),
                   ),
            )

    global_clamp_size: bpy.props.FloatProperty(
            name="Clamp Size",
            description="Clamp bounds under this value (zero to disable)",
            min=0.0, max=1000.0,
            soft_min=0.0, soft_max=1000.0,
            default=0.0,
            )

    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import import_obj

        if self.split_mode == 'OFF':
            self.use_split_objects = False
            self.use_split_groups = False
        else:
            self.use_groups_as_vgroups = False

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "split_mode",
                                            ))

        global_matrix = axis_conversion(from_forward=self.axis_forward,
                                        from_up=self.axis_up,
                                        ).to_4x4()
        keywords["global_matrix"] = global_matrix

        if bpy.data.is_saved and context.user_preferences.filepaths.use_relative_paths:
            import os
            keywords["relpath"] = os.path.dirname(bpy.data.filepath)

        return import_obj.load(context, **keywords)

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "use_smooth_groups")
        row.prop(self, "use_edges")

        box = layout.box()
        row = box.row()
        row.prop(self, "split_mode", expand=True)

        row = box.row()
        if self.split_mode == 'ON':
            row.label(text="Split by:")
            row.prop(self, "use_split_objects")
            row.prop(self, "use_split_groups")
        else:
            row.prop(self, "use_groups_as_vgroups")

        row = layout.split(percentage=0.67)
        row.prop(self, "global_clamp_size")
        layout.prop(self, "axis_forward")
        layout.prop(self, "axis_up")

        layout.prop(self, "use_image_search")


@orientation_helper(axis_forward='-Z', axis_up='Y')
class ExportXpsNgff(bpy.types.Operator, ExportHelper):
    """Save a Wavefront OBJ File."""

    bl_idname = "export_xps_ngff.obj"
    bl_label = 'Export XPS NGFF'
    bl_options = {'PRESET'}

    filename_ext = ".obj"
    filter_glob: bpy.props.StringProperty(
            default="*.obj;*.mtl;*.arl",
            options={'HIDDEN'},
            )

    # context group
    use_selection: bpy.props.BoolProperty(
            name="Selection Only",
            description="Export selected objects only",
            default=False,
            )
    use_animation: bpy.props.BoolProperty(
            name="Animation",
            description="Write out an OBJ for each frame",
            default=False,
            )

    # object group
    use_mesh_modifiers: bpy.props.BoolProperty(
            name="Apply Modifiers",
            description="Apply modifiers (preview resolution)",
            default=True,
            )

    # extra data group
    use_edges: bpy.props.BoolProperty(
            name="Include Edges",
            description="",
            default=True,
            )
    use_smooth_groups: bpy.props.BoolProperty(
            name="Smooth Groups",
            description="Write sharp edges as smooth groups",
            default=False,
            )
    use_smooth_groups_bitflags: bpy.props.BoolProperty(
            name="Bitflag Smooth Groups",
            description="Same as 'Smooth Groups', but generate smooth groups IDs as bitflags "
                        "(produces at most 32 different smooth groups, usually much less)",
            default=False,
            )
    use_normals: bpy.props.BoolProperty(
            name="Write Normals",
            description="Export one normal per vertex and per face, to represent flat faces and sharp edges",
            default=True,
            )
    use_vcolors: bpy.props.BoolProperty(
            name="Write Vert Colors",
            description="Export Vertex Color",
            default=True,
            )
    use_uvs: bpy.props.BoolProperty(
            name="Include UVs",
            description="Write out the active UV coordinates",
            default=True,
            )
    use_materials: bpy.props.BoolProperty(
            name="Write Materials",
            description="Write out the MTL file",
            default=True,
            )
    use_triangles: bpy.props.BoolProperty(
            name="Triangulate Faces",
            description="Convert all faces to triangles",
            default=False,
            )
    use_nurbs: bpy.props.BoolProperty(
            name="Write Nurbs",
            description="Write nurbs curves as OBJ nurbs rather than "
                        "converting to geometry",
            default=False,
            )
    use_vertex_groups: bpy.props.BoolProperty(
            name="Polygroups",
            description="",
            default=False,
            )

    # grouping group
    use_blen_objects: bpy.props.BoolProperty(
            name="Objects as OBJ Objects",
            description="",
            default=True,
            )
    group_by_object: bpy.props.BoolProperty(
            name="Objects as OBJ Groups ",
            description="",
            default=False,
            )
    group_by_material: bpy.props.BoolProperty(
            name="Material Groups",
            description="",
            default=False,
            )
    keep_vertex_order: bpy.props.BoolProperty(
            name="Keep Vertex Order",
            description="",
            default=False,
            )
    global_scale: bpy.props.FloatProperty(
            name="Scale",
            min=0.01, max=1000.0,
            default=1.0,
            )

    path_mode = path_reference_mode

    check_extension = True

    def execute(self, context):
        from . import export_obj

        from mathutils import Matrix
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            ))

        global_matrix = (Matrix.Scale(self.global_scale, 4) *
                         axis_conversion(to_forward=self.axis_forward,
                                         to_up=self.axis_up,
                                         ).to_4x4())

        keywords["global_matrix"] = global_matrix
        return export_obj.save(context, **keywords)


class XpsImportSubMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_xnalara_import_submenu"
    bl_label = "XNALara / XPS"

    def draw(self, context):
        layout = self.layout
        layout.operator(Import_Xps_Model_Op.bl_idname, text="XNALara/XPS Model (.ascii/.mesh/.xps)")
        layout.operator(Import_Xps_Pose_Op.bl_idname, text="XNALara/XPS Pose (.pose)")
        layout.operator(ImportXpsNgff.bl_idname, text="XPS NGFF (.obj)")


class XpsExportSubMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_xnalara_export_submenu"
    bl_label = "XNALara / XPS"

    def draw(self, context):
        layout = self.layout
        layout.operator(Export_Xps_Model_Op.bl_idname, text="XNALara/XPS Model (.ascii/.mesh/.xps)")
        layout.operator(Export_Xps_Pose_Op.bl_idname, text="XNALara/XPS Pose (.pose)")
        layout.operator(ExportXpsNgff.bl_idname, text="XPS NGFF (.obj)")


#
# Registration
#
def menu_func_import(self, context):
    my_icon = custom_icons["main"]["xps_icon"]
    self.layout.menu(XpsImportSubMenu.bl_idname, icon_value=my_icon.icon_id)


def menu_func_export(self, context):
    my_icon = custom_icons["main"]["xps_icon"]
    self.layout.menu(XpsExportSubMenu.bl_idname, icon_value=my_icon.icon_id)


# --------------------------------------------------------------------------------
#  Custom Icons
# --------------------------------------------------------------------------------
custom_icons = {}


def registerCustomIcon():
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    script_path = os.path.dirname(__file__)
    icons_dir = os.path.join(script_path, "icons")
    pcoll.load("xps_icon", os.path.join(icons_dir, "icon.png"), 'IMAGE')
    custom_icons["main"] = pcoll


def unregisterCustomIcon():
    for pcoll in custom_icons.values():
        bpy.utils.previews.remove(pcoll)
    custom_icons.clear()


def register():
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    registerCustomIcon()


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    unregisterCustomIcon()


if __name__ == "__main__":
    register()
