# -*- coding: utf-8 -*-
# <pep8 compliant>

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "johnzero7",
    "version": (1, 8, 4),
    "blender": (2, 74, 0),
    "location": "File > Import-Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "",
	"wiki_url":    "https://github.com/johnzero7/xps_tools",
	"tracker_url": "https://github.com/johnzero7/xps_tools/issues",
    "category": "Import-Export",
}

if "bpy" in locals():
    import importlib
    # Import if the library is new
    from . import xps_tools
    from . import xps_toolshelf
    from . import xps_const
    from . import xps_types
    from . import xps_material
    from . import write_ascii_xps
    from . import write_bin_xps
    from . import read_ascii_xps
    from . import read_bin_xps
    from . import mock_xps_data
    from . import export_xnalara_model
    from . import export_xnalara_pose
    from . import import_xnalara_model
    from . import import_xnalara_pose
    from . import import_obj
    from . import export_obj
    from . import ascii_ops
    from . import bin_ops
    from . import timing
    from . import material_converter
    from . import addon_updater_ops
    # Reload
    importlib.reload(xps_tools)
    importlib.reload(xps_toolshelf)
    importlib.reload(xps_const)
    importlib.reload(xps_types)
    importlib.reload(xps_material)
    importlib.reload(write_ascii_xps)
    importlib.reload(write_bin_xps)
    importlib.reload(read_ascii_xps)
    importlib.reload(read_bin_xps)
    importlib.reload(mock_xps_data)
    importlib.reload(export_xnalara_model)
    importlib.reload(export_xnalara_pose)
    importlib.reload(import_xnalara_model)
    importlib.reload(import_xnalara_pose)
    importlib.reload(import_obj)
    importlib.reload(export_obj)
    importlib.reload(ascii_ops)
    importlib.reload(bin_ops)
    importlib.reload(timing)
    importlib.reload(material_converter)
    importlib.reload(addon_updater_ops)
    # print("Reloading Libraries")
else:
    import bpy
    from . import xps_tools
    from . import xps_toolshelf
    from . import xps_const
    from . import xps_types
    from . import xps_material
    from . import write_ascii_xps
    from . import write_bin_xps
    from . import read_ascii_xps
    from . import read_bin_xps
    from . import mock_xps_data
    from . import export_xnalara_model
    from . import export_xnalara_pose
    from . import import_xnalara_model
    from . import import_xnalara_pose
    from . import ascii_ops
    from . import bin_ops
    from . import timing
    from . import material_converter
    from . import addon_updater_ops
    # print("Loading Libraries")


class DemoPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__


    # addon updater preferences from `__init__`, be sure to copy all of them
    auto_check_update = bpy.props.BoolProperty(
        name = "Auto-check for Update",
        description = "If enabled, auto-check for updates using an interval",
        default = False,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description = "Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description = "Number of days between checking for updates",
        default=7,
        min=0,
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description = "Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description = "Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )


    def draw(self, context):
        layout = self.layout
        addon_updater_ops.update_settings_ui(self, context)

#
# Registration
#


def register():
    # print('Registering %s' % __name__)
    bpy.utils.register_module(__name__)
    xps_tools.register()
    addon_updater_ops.register(bl_info)


def unregister():
    # print('Unregistering %s' % __name__)
    addon_updater_ops.unregister()
    xps_tools.unregister()
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

    # call exporter
    # bpy.ops.xps_tools.export_model('INVOKE_DEFAULT')

    # call importer
    # bpy.ops.xps_tools.import_model('INVOKE_DEFAULT')
