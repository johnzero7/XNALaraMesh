# -*- coding: utf-8 -*-
# <pep8 compliant>

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "johnzero7",
    "version": (1, 9, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "",
	"wiki_url":    "https://github.com/johnzero7/xps_tools",
	"tracker_url": "https://github.com/johnzero7/xps_tools/issues",
    "category": "Import-Export",
}


#############################################
# support reloading sub-modules
_modules = [
    'xps_panels',
    'xps_tools',
    'xps_toolshelf',
    'xps_const',
    'xps_types',
    'xps_material',
    'write_ascii_xps',
    'write_bin_xps',
    'read_ascii_xps',
    'read_bin_xps',
    'mock_xps_data',
    'export_xnalara_model',
    'export_xnalara_pose',
    'import_xnalara_model',
    'import_xnalara_pose',
    'import_obj',
    'export_obj',
    'ascii_ops',
    'bin_ops',
    'timing',
    'material_creator',
    'addon_updater_ops'
]

#Reload previously loaded modules
if "bpy" in locals():
    from importlib import reload
    _modules_loaded[:] = [reload(module) for module in _modules_loaded]
    del reload


#First import the modules
__import__(name=__name__, fromlist=_modules)
_namespace = globals()
_modules_loaded = [_namespace[name] for name in _modules]
del _namespace
# support reloading sub-modules
#############################################

import bpy


class UpdaterPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__


    # addon updater preferences from `__init__`, be sure to copy all of them
    auto_check_update : bpy.props.BoolProperty(
        name = "Auto-check for Update",
        description = "If enabled, auto-check for updates using an interval",
        default = False,
    )
    updater_intrval_months : bpy.props.IntProperty(
        name='Months',
        description = "Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days : bpy.props.IntProperty(
        name='Days',
        description = "Number of days between checking for updates",
        default=7,
        min=0,
    )
    updater_intrval_hours : bpy.props.IntProperty(
        name='Hours',
        description = "Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes : bpy.props.IntProperty(
        name='Minutes',
        description = "Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )


    def draw(self, context):
        addon_updater_ops.update_settings_ui(self, context)

#
# Registration
#


classesToRegister = [
    UpdaterPreferences,
    xps_panels.XPSToolsObjectPanel,
    xps_panels.XPSToolsBonesPanel,
    xps_panels.XPSToolsAnimPanel,

    xps_toolshelf.ArmatureBonesHideByName_Op,
    xps_toolshelf.ArmatureBonesHideByVertexGroup_Op,
    xps_toolshelf.ArmatureBonesShowAll_Op,
    xps_toolshelf.ArmatureBonesRenameToBlender_Op,
    xps_toolshelf.ArmatureBonesRenameToXps_Op,
    xps_toolshelf.ArmatureBonesConnect_Op,
    xps_toolshelf.NewRestPose_Op,

    xps_tools.Import_Xps_Model_Op,
    xps_tools.Export_Xps_Model_Op,
    xps_tools.Import_Xps_Pose_Op,
    xps_tools.Export_Xps_Pose_Op,
    xps_tools.Import_Poses_To_Keyframes_Op,
    xps_tools.Export_Frames_To_Poses_Op,
    xps_tools.ArmatureBoneDictGenerate_Op,
    xps_tools.ArmatureBoneDictRename_Op,
    xps_tools.ArmatureBoneDictRestore_Op,
    xps_tools.ImportXpsNgff,
    xps_tools.ExportXpsNgff,
    xps_tools.XpsImportSubMenu,
    xps_tools.XpsExportSubMenu,
]


#Use factory to create method to register and unregister the classes
registerClasses, unregisterClasses = bpy.utils.register_classes_factory(classesToRegister)


def register():
    registerClasses()
    xps_tools.register()
    addon_updater_ops.register(bl_info)


def unregister():
    addon_updater_ops.unregister()
    xps_tools.unregister()
    unregisterClasses()


if __name__ == "__main__":
    register()

    # call exporter
    # bpy.ops.xps_tools.export_model('INVOKE_DEFAULT')

    # call importer
    # bpy.ops.xps_tools.import_model('INVOKE_DEFAULT')
