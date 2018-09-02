# -*- coding: utf-8 -*-
# <pep8 compliant>

import bpy

from . import import_xnalara_model
from . import import_xnalara_pose
from bpy.props import BoolProperty


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
    bl_description = 'Rename bones to Blender bone name convention (left -> .L)'
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
    bl_description = 'Rename bones back to XPS (.L -> left)'
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

    connectBones : bpy.props.BoolProperty()

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
            bpy.context.view_layer.objects.active = armature_ob
            import_xnalara_model.setBoneConnect(self.connectBones)
        bpy.context.view_layer.objects.active = activeObj
        return {'FINISHED'}


class NewRestPose_Op(bpy.types.Operator):
    bl_idname = 'xps_tools.new_rest_pose'
    bl_label = 'New Rest Pose'
    bl_description = 'Set Current Pose as The New Rest Pose'
    bl_options = {"PRESET"}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'ARMATURE' and
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
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply( modifier = destModif.name )

        bpy.context.view_layer.objects.active = activeArmature
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

