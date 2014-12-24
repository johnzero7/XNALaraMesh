# -*- coding: utf-8 -*-

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty

class XPSToolsObjectPanel(bpy.types.Panel):
    '''XPS Toolshelf'''
    bl_idname = 'OBJECT_PT_xps_tools_object'
    bl_label = 'XPS Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'XPS'
    bl_context = 'objectmode'

    def draw(self, context):
        #active_obj = context.active_object
        mesh_obj = next((obj for obj in context.selected_objects if obj.type == 'MESH'), None)
        armature_obj = next((obj for obj in context.selected_objects if obj.type == 'ARMATURE'), None)

        layout = self.layout

        col = layout.column()

        col.label('Import:')
        c = col.column()
        r = c.row(align=True)
        r.operator('xps_tools.import_model', text='Model')
        if armature_obj is not None:
            r.operator('xps_tools.import_pose', text='Pose')
        col.separator()

        if mesh_obj is not None or armature_obj is not None:
            col.label(text="Export:")
            c = col.column()
            r = c.row(align=True)
            if mesh_obj is not None:
                r.operator('xps_tools.export_model', text='Model')
            if armature_obj is not None:
                r.operator('xps_tools.export_pose', text='Pose')

        col = layout.column()
        col.label('View:')
        c = col.column(align=True)
        r = c.row(align=True)
        r.operator('xps_tools.set_glsl_shading', text='GLSL')
        r.operator('xps_tools.set_shadeless_glsl_shading', text='Shadeless')
        r = c.row(align=True)
        #r.operator('xps_tools.set_cycles_rendering', text='Cycles')
        r.operator('xps_tools.reset_shading', text='Reset')



class SetGLSLShading_Op(bpy.types.Operator):
    '''GLSL Shading Display'''
    bl_idname = 'xps_tools.set_glsl_shading'
    bl_label = 'GLSL View'
    bl_description = 'Change Display to GLSL'
    bl_options = {'PRESET'}

    def execute(self, context):
        bpy.ops.xps_tools.reset_shading()
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        for i in filter(lambda x: x.type == 'MESH', context.scene.objects):
            for s in i.material_slots:
                s.material.use_shadeless = False

        context.area.spaces[0].viewport_shade='TEXTURED'
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
        for i in filter(lambda x: x.type == 'MESH', context.scene.objects):
            for s in i.material_slots:
                s.material.use_shadeless = True

        try:
            bpy.context.scene.display_settings.display_device = 'None'
        except TypeError:
            pass # Blender was built without OpenColorIO
        context.area.spaces[0].viewport_shade='TEXTURED'
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
        for i in filter(lambda x: x.type == 'MESH', context.scene.objects):
            cycles_converter.convertToCyclesShader(i)
        context.area.spaces[0].viewport_shade='MATERIAL'
        return {'FINISHED'}

class ResetShading_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.reset_shading'
    bl_label = 'Reset View'
    bl_description = ''
    bl_options = {'PRESET'}

    def execute(self, context):
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        for i in filter(lambda x: x.type == 'MESH', context.scene.objects):
            for s in i.material_slots:
                s.material.use_shadeless = False
                s.material.use_nodes = False

        bpy.context.scene.display_settings.display_device = 'sRGB'
        context.area.spaces[0].viewport_shade='SOLID'
        bpy.context.scene.game_settings.material_mode = 'MULTITEXTURE'
        return {'FINISHED'}

class SetShadelessMaterials_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.set_shadeless_materials'
    bl_label = 'GLSL View'
    bl_description = 'set the materials of selected objects to shadeless.'
    bl_options = {'PRESET'}

    def execute(self, context):
        for i in context.selected_objects:
            for s in i.material_slots:
                s.material.use_shadeless = True
        return {'FINISHED'}

#
# Registration
#
def register():
    bpy.utils.register_class(XPSToolsObjectPanel)
    bpy.utils.register_class(SetGLSLShading_Op)
    bpy.utils.register_class(SetShadelessGLSLShading_Op)
    bpy.utils.register_class(SetCyclesRendering_Op)
    bpy.utils.register_class(ResetShading_Op)
    bpy.utils.register_class(SetShadelessMaterials_Op)

   
def unregister():

    bpy.utils.unregister_class(XPSToolsObjectPanel)
    bpy.utils.unregister_class(SetGLSLShading_Op)
    bpy.utils.unregister_class(SetShadelessGLSLShading_Op)
    bpy.utils.unregister_class(SetCyclesRendering_Op)
    bpy.utils.unregister_class(ResetShading_Op)
    bpy.utils.unregister_class(SetShadelessMaterials_Op)


if __name__ == "__main__":
    register()

