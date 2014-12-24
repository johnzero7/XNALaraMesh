# -*- coding: utf-8 -*-

from . import xps_tools
from . import xps_toolshelf
import bpy

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "johnzero7",
    "version": (1, 0),
    "blender": (2, 7, 0),
    "location": "File > Import/Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}
    
if "bpy" in locals():
    import imp
    if 'xps_tools' in locals():
        imp.reload(xps_tools)
    if 'xps_toolshelf' in locals():
        imp.reload(xps_toolshelf)

#import os, sys
#cmd_folder = os.path.dirname(os.path.abspath(__file__))
#if cmd_folder not in sys.path:
#    sys.path.insert(0, cmd_folder)


#
# Registration
#
def register():
    print('Registering %s' % __name__)
    xps_tools.register()
    xps_toolshelf.register()
    #bpy.utils.register_class(xps_tools.XPSToolsDummyClass)
    #bpy.utils.register_module(xps_tools)
    #bpy.utils.register_module(xps_toolshelf)

def unregister():
    print('Unregistering %s' % __name__)
    xps_tools.unregister()
    xps_toolshelf.unregister()
    #bpy.utils.unregister_class(xps_tools.XPSToolsDummyClass)
    #bpy.utils.unregister_module(xps_tools)
    #bpy.utils.unregister_module(xps_toolshelf)

if __name__ == "__main__":
    register()
    
    #call exporter
    bpy.ops.xps_tools.export_model('INVOKE_DEFAULT')

    #call importer
    #bpy.ops.xps_tools.import_model('INVOKE_DEFAULT')









