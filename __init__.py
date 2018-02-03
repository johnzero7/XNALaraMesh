# -*- coding: utf-8 -*-
# <pep8 compliant>

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "johnzero7",
    "version": (1, 8, 2),
    "blender": (2, 74, 0),
    "location": "File > Import-Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "",
	"wiki_url":    "https://github.com/johnzero7/xps_tools",
	"tracker_url": "https://github.com/johnzero7/xps_tools/issues",
    "category": "Import-Export",
}

if "bpy" in locals():
    import imp
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
    imp.reload(xps_tools)
    imp.reload(xps_toolshelf)
    imp.reload(xps_const)
    imp.reload(xps_types)
    imp.reload(xps_material)
    imp.reload(write_ascii_xps)
    imp.reload(write_bin_xps)
    imp.reload(read_ascii_xps)
    imp.reload(read_bin_xps)
    imp.reload(mock_xps_data)
    imp.reload(export_xnalara_model)
    imp.reload(export_xnalara_pose)
    imp.reload(import_xnalara_model)
    imp.reload(import_xnalara_pose)
    imp.reload(import_obj)
    imp.reload(export_obj)
    imp.reload(ascii_ops)
    imp.reload(bin_ops)
    imp.reload(timing)
    imp.reload(material_converter)
    imp.reload(addon_updater_ops)
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
