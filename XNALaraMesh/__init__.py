# -*- coding: utf-8 -*-

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "johnzero7",
    "version": (1, 5, 0),
    "blender": (2, 7, 0),
    "location": "File > Import/Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    # Import if the library is new
    from XNALaraMesh import xps_tools
    from XNALaraMesh import xps_toolshelf
    from XNALaraMesh import xps_const
    from XNALaraMesh import xps_types
    from XNALaraMesh import xps_material
    from XNALaraMesh import write_ascii_xps
    from XNALaraMesh import write_bin_xps
    from XNALaraMesh import read_ascii_xps
    from XNALaraMesh import read_bin_xps
    from XNALaraMesh import mock_xps_data
    from XNALaraMesh import export_xnalara_model
    from XNALaraMesh import export_xnalara_pose
    from XNALaraMesh import import_xnalara_model
    from XNALaraMesh import import_xnalara_pose
    from XNALaraMesh import ascii_ops
    from XNALaraMesh import bin_ops
    from XNALaraMesh import timing
    from XNALaraMesh import material_converter
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
    imp.reload(ascii_ops)
    imp.reload(bin_ops)
    imp.reload(timing)
    imp.reload(material_converter)
    # print("Reloading Libraries")
else:
    from XNALaraMesh import xps_tools
    from XNALaraMesh import xps_toolshelf
    from XNALaraMesh import xps_const
    from XNALaraMesh import xps_types
    from XNALaraMesh import xps_material
    from XNALaraMesh import write_ascii_xps
    from XNALaraMesh import write_bin_xps
    from XNALaraMesh import read_ascii_xps
    from XNALaraMesh import read_bin_xps
    from XNALaraMesh import mock_xps_data
    from XNALaraMesh import export_xnalara_model
    from XNALaraMesh import export_xnalara_pose
    from XNALaraMesh import import_xnalara_model
    from XNALaraMesh import import_xnalara_pose
    from XNALaraMesh import ascii_ops
    from XNALaraMesh import bin_ops
    from XNALaraMesh import timing
    from XNALaraMesh import material_converter
    # print("Loading Libraries")

import bpy

#
# Registration
#


def register():
    # print('Registering %s' % __name__)
    bpy.utils.register_module(__name__)
    xps_tools.register()
    # bpy.utils.register_class(xps_tools.XPSToolsDummyClass)
    # bpy.utils.register_module(xps_tools)
    # bpy.utils.register_module(xps_toolshelf)


def unregister():
    # print('Unregistering %s' % __name__)
    bpy.utils.unregister_module(__name__)
    xps_tools.unregister()
    # bpy.utils.unregister_class(xps_tools.XPSToolsDummyClass)
    # bpy.utils.unregister_module(xps_tools)
    # bpy.utils.unregister_module(xps_toolshelf)

if __name__ == "__main__":
    register()

    # call exporter
    # bpy.ops.xps_tools.export_model('INVOKE_DEFAULT')

    # call importer
    # bpy.ops.xps_tools.import_model('INVOKE_DEFAULT')
