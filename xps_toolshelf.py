# -*- coding: utf-8 -*-
# <pep8 compliant>

from . import import_xnalara_model
from . import import_xnalara_pose
import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper
from bpy_extras.io_utils import ImportHelper


class XPSToolsObjectPanel(bpy.types.Panel):

    '''XPS Toolshelf'''
    bl_idname = 'OBJECT_PT_xps_tools_object'
    bl_label = 'XPS Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'XPS'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.label('Import:')
        # c = col.column()
        r = col.row(align=True)
        r1c1 = r.column(align=True)
        r1c1.operator("xps_tools.import_model", text='Model', icon='NONE')
        r1c2 = r.column(align=True)
        r1c2.operator('xps_tools.import_pose', text='Pose')

        # col.separator()
        col = layout.column()

        col.label(text="Export:")
        c = col.column()
        r = c.row(align=True)
        r2c1 = r.column(align=True)
        r2c1.operator('xps_tools.export_model', text='Model')
        r2c2 = r.column(align=True)
        r2c2.operator('xps_tools.export_pose', text='Pose')

        # col.separator()
        col = layout.column()

        col.label('View:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.set_glsl_shading', text='GLSL')
        r.operator('xps_tools.set_shadeless_glsl_shading', text='Shadeless')
        r = c.row(align=True)
        # r.operator('xps_tools.set_cycles_rendering', text='Cycles')
        r.operator('xps_tools.reset_shading', text='Reset')


class XPSToolsBonesPanel(bpy.types.Panel):

    '''XPS Toolshelf'''
    bl_idname = 'OBJECT_PT_xps_tools_bones'
    bl_label = 'XPS Bones'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'XPS'
    bl_context = 'objectmode'

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # col.separator()
        col = layout.column()

        col.label('Hide Bones:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.bones_hide_by_name', text='Unused')
        r.operator('xps_tools.bones_hide_by_vertex_group', text='Vertex Group')
        r = c.row(align=True)
        # r.operator('xps_tools.set_cycles_rendering', text='Cycles')
        r.operator('xps_tools.bones_show_all', text='Show All')

        # col.separator()
        col = layout.column()

        col.label('BoneDict:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.bones_dictionary_rename', text='Rename Bones')
        r = c.row(align=True)
        r.operator('xps_tools.bones_dictionary_restore_name', text='Restore Names')

        # col.separator()
        col = layout.column()

        col.label('Rename Bones:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.bones_rename_to_blender', text='XPS to Blender')
        r = c.row(align=True)
        r.operator('xps_tools.bones_rename_to_xps', text='Blender To XPS')

        col = layout.column()

        col.label('Connect Bones:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator(
            'xps_tools.bones_connect',
            text='Connect All').connectBones = True
        r = c.row(align=True)
        r.operator(
            'xps_tools.bones_connect',
            text='Disconnect All').connectBones = False
        col.label('New Rest Pose:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator(
            'xps_tools.new_rest_pose',
            text='New Rest Pose')


class XPSToolsAnimPanel(bpy.types.Panel):

    '''XPS Toolshelf'''
    bl_idname = 'OBJECT_PT_xps_tools_anim'
    bl_label = 'XPS Anim'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'XPS'
    bl_context = 'objectmode'

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # col.separator()
        col = layout.column()

        col.label('Import:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator(
            'xps_tools.import_poses_to_keyframes',
            text='Poses to Keyframes')

        # col.separator()
        col = layout.column()

        col.label('Export:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.export_frames_to_poses', text='Frames to Poses')


class XPSToolsMaterialConverterPanel(bpy.types.Panel):

    '''XPS Toolshelf'''
    bl_idname = 'OBJECT_PT_xps_material_converter'
    bl_label = 'XPS Material Converter'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'XPS'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        sceneContext = context.scene
        c = col.column(align=True)
        c.label('Material Converter:')
        r = c.row(align=True)
        r.operator("xps_tools.convert_to_cycles_all", text='All Materials to Cycles')
        r = c.row(align=True)
        r.operator("xps_tools.convert_to_cycles_selected", text='Selected Materials to Cycles')
        r = layout.row()
        r.operator("xps_tools.restore_bi_materials_all", text='Restore Blender Internal')


class SetGLSLShading_Op(bpy.types.Operator):

    '''GLSL Shading Display'''
    bl_idname = 'xps_tools.set_glsl_shading'
    bl_label = 'GLSL View'
    bl_description = 'Change Display to GLSL'
    bl_options = {'PRESET'}

    def execute(self, context):
        bpy.ops.xps_tools.reset_shading()
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        for mesh_ob in filter(lambda obj: obj.type == 'MESH', context.scene.objects):
            for mat_slot in mesh_ob.material_slots:
                if mat_slot.material:
                    mat_slot.material.use_shadeless = False

        context.area.spaces[0].viewport_shade = 'TEXTURED'
        bpy.context.scene.game_settings.material_mode = 'GLSL'
        return {'FINISHED'}


class SetShadelessGLSLShading_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.set_shadeless_glsl_shading'
    bl_label = 'Shadeless GLSL View'
    bl_description = 'Set Materials to Shadeless'
    bl_options = {'PRESET'}

    def execute(self, context):
        bpy.ops.xps_tools.reset_shading()
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        for mesh_ob in filter(lambda obj: obj.type == 'MESH', context.scene.objects):
            for mat_slot in mesh_ob.material_slots:
                if mat_slot.material:
                    mat_slot.material.use_shadeless = True

        try:
            bpy.context.scene.display_settings.display_device = 'None'
        except TypeError:
            pass  # Blender was built without OpenColorIO
        context.area.spaces[0].viewport_shade = 'TEXTURED'
        bpy.context.scene.game_settings.material_mode = 'GLSL'
        return {'FINISHED'}


class SetCyclesRendering_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.set_cycles_rendering'
    bl_label = 'Cycles'
    bl_description = 'Convert blender render shader to Cycles shader'
    bl_options = {'PRESET'}

    def execute(self, context):
        bpy.ops.xps_tools.reset_shading()
        bpy.context.scene.render.engine = 'CYCLES'
        for mesh_ob in filter(lambda obj: obj.type == 'MESH', context.scene.objects):
            cycles_converter.convertToCyclesShader(mesh_ob)
        context.area.spaces[0].viewport_shade = 'MATERIAL'
        return {'FINISHED'}


class ResetShading_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.reset_shading'
    bl_label = 'Reset View'
    bl_description = ''
    bl_options = {'PRESET'}

    def execute(self, context):
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        for mesh_ob in filter(lambda obj: obj.type == 'MESH', context.scene.objects):
            for mat_slot in mesh_ob.material_slots:
                if mat_slot.material:
                    mat_slot.material.use_shadeless = False
                    mat_slot.material.use_nodes = False

        bpy.context.scene.display_settings.display_device = 'sRGB'
        context.area.spaces[0].viewport_shade = 'SOLID'
        bpy.context.scene.game_settings.material_mode = 'MULTITEXTURE'
        return {'FINISHED'}


class SetShadelessMaterials_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.set_shadeless_materials'
    bl_label = 'GLSL View'
    bl_description = 'set the materials of selected objects to shadeless.'
    bl_options = {'PRESET'}

    def execute(self, context):
        for obj in context.selected_objects:
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    mat_slot.material.use_shadeless = True
        return {'FINISHED'}


class ArmatureBonesHideByName_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_hide_by_name'
    bl_label = 'Hide bones by name'
    bl_description = 'Move bones starting with "unused" to the armature layer 2'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        import_xnalara_model.hideBonesByName(self.armature_objs)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.armature_objs = [
            obj for obj in context.selected_objects if obj.type == 'ARMATURE']
        return self.execute(context)

    def check(self, context):
        print('CHECK')
        return {'RUNNING_MODAL'}


class ArmatureBonesHideByVertexGroup_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_hide_by_vertex_group'
    bl_label = 'Hide bones by weight'
    bl_description = 'Move bones that do not alter any mesh to the armature layer 2'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        import_xnalara_model.hideBonesByVertexGroup(self.armature_objs)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.armature_objs = [
            obj for obj in context.selected_objects if obj.type == 'ARMATURE']
        return self.execute(context)

    def check(self, context):
        print('CHECK')
        return {'RUNNING_MODAL'}


class ArmatureBonesShowAll_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_show_all'
    bl_label = 'Show all Bones'
    bl_description = 'Move all bones to the armature layer 1'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        import_xnalara_model.showAllBones(self.armature_objs)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.armature_objs = [
            obj for obj in context.selected_objects if obj.type == 'ARMATURE']
        return self.execute(context)

    def check(self, context):
        print('CHECK')
        return {'RUNNING_MODAL'}


class ArmatureBonesRenameToBlender_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_rename_to_blender'
    bl_label = 'Rename Bones'
    bl_description = 'Rename bones to Blender bone name convention'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        armatures_obs = filter(
            lambda obj: obj.type == 'ARMATURE',
            context.selected_objects)
        import_xnalara_pose.renameBonesToBlender(armatures_obs)
        return {'FINISHED'}


class ArmatureBonesRenameToXps_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_rename_to_xps'
    bl_label = 'Rename Bones'
    bl_description = 'Rename bones back to XPS'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        armatures_obs = filter(
            lambda obj: obj.type == 'ARMATURE',
            context.selected_objects)
        import_xnalara_pose.renameBonesToXps(armatures_obs)
        return {'FINISHED'}


class ArmatureBonesConnect_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.bones_connect'
    bl_label = 'Set Bones Connection'
    bl_description = 'Set Bones Connection'
    bl_options = {'PRESET'}

    connectBones = bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bool(
            next(
                (obj for obj in context.selected_objects if obj.type == 'ARMATURE'),
                None))

    def execute(self, context):
        armatures_obs = filter(
            lambda obj: obj.type == 'ARMATURE',
            context.selected_objects)
        activeObj = bpy.context.active_object
        for armature_ob in armatures_obs:
            bpy.context.scene.objects.active = armature_ob
            import_xnalara_model.setBoneConnect(self.connectBones)
        bpy.context.scene.objects.active = activeObj
        return {'FINISHED'}


class NewRestPose_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.new_rest_pose'
    bl_label = 'New Rest Pose'
    bl_description = 'Set Current Pose as The New Rest Pose'
    bl_options = {"PRESET"}

    @classmethod
    def poll(cls, context):
        return (bool(context.active_object.type == 'ARMATURE') and
                bool(next(
                (obj for obj in context.selected_objects if obj.type == 'MESH'),
                None)))

    def action_common(self, context) :
        meshes_obs = filter(lambda obj: obj.type == 'MESH', context.selected_objects)
        activeArmature = context.active_object
        for obj in meshes_obs:
            if (obj.find_armature() == activeArmature):
                sourceModif = obj.modifiers[-1]
                if (sourceModif and sourceModif.type == 'ARMATURE'):
                    destModif = obj.modifiers.new(sourceModif.name, sourceModif.type)

                    # collect names of writable properties
                    properties = [p.identifier for p in destModif.bl_rna.properties
                                  if not p.is_readonly]

                    # copy those properties
                    for prop in properties:
                        setattr(destModif, prop, getattr(sourceModif, prop))

                    print(destModif.name)
                    bpy.context.scene.objects.active = obj
                    bpy.ops.object.modifier_apply( modifier = destModif.name )

        bpy.context.scene.objects.active = activeArmature
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')


    #end action_common

    def execute(self, context) :
        self.action_common(context)
        return {"FINISHED"}
    #end execute

    def invoke(self, context, event) :
        self.action_common(context)
        return {"FINISHED"}
    #end invoke

