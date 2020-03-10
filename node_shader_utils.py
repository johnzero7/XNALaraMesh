import bpy
from bpy_extras import node_shader_utils

class XPSShaderWrapper(node_shader_utils.ShaderWrapper):
    """
    Hard coded shader setup, based in XPS Shader.
    Should cover most common cases on import, and gives a basic nodal shaders support for export.
    """
    NODES_LIST = (
        "node_out",
        "node_principled_bsdf",

        "_node_normalmap",
        "_node_texcoords",
    )

    __slots__ = (
        "is_readonly",
        "material",
        *NODES_LIST,
    )

    NODES_LIST = node_shader_utils.ShaderWrapper.NODES_LIST + NODES_LIST

    def __init__(self, material, is_readonly=True, use_nodes=True):
        super(XPSShaderWrapper, self).__init__(material, is_readonly, use_nodes)


    def update(self):
        super(XPSShaderWrapper, self).update()

        if not self.use_nodes:
            return

        tree = self.material.node_tree

        nodes = tree.nodes
        links = tree.links

        # --------------------------------------------------------------------
        # Main output and shader.
        node_out = None
        node_principled = None
        for n in nodes:
            #print("loop:",n.name)
            if n.bl_idname == 'ShaderNodeOutputMaterial' and n.inputs[0].is_linked:
                #print("output found:")
                node_out = n
                node_principled = n.inputs[0].links[0].from_node
            elif n.bl_idname == 'ShaderNodeGroup' and n.node_tree.name == 'XPS Shader' and n.outputs[0].is_linked:
                #print("xps shader found")
                node_principled = n
                for lnk in n.outputs[0].links:
                    node_out = lnk.to_node
                    if node_out.bl_idname == 'ShaderNodeOutputMaterial':
                        break
            if (
                    node_out is not None and node_principled is not None and
                    node_out.bl_idname == 'ShaderNodeOutputMaterial' and
                    node_principled.bl_idname == 'ShaderNodeGroup' and node_principled.node_tree.name == 'XPS Shader'
            ):
                break
            node_out = node_principled = None  # Could not find a valid pair, let's try again

        if node_out is not None:
            self._grid_to_location(0, 0, ref_node=node_out)
        elif not self.is_readonly:
            node_out = nodes.new(type='ShaderNodeOutputMaterial')
            node_out.label = "Material Out"
            node_out.target = 'ALL'
            self._grid_to_location(1, 1, dst_node=node_out)
        self.node_out = node_out

        if node_principled is not None:
            self._grid_to_location(0, 0, ref_node=node_principled)
        elif not self.is_readonly:
            node_principled = nodes.new(type='XPS Shader')
            node_principled.label = "Principled BSDF"
            self._grid_to_location(0, 1, dst_node=node_principled)
            # Link
            links.new(node_principled.outputs["BSDF"], self.node_out.inputs["Surface"])
        self.node_principled_bsdf = node_principled

        # --------------------------------------------------------------------
        # Normal Map, lazy initialization...
        self._node_normalmap = ...

        # --------------------------------------------------------------------
        # Tex Coords, lazy initialization...
        self._node_texcoords = ...


    # --------------------------------------------------------------------
    # Get Image Node.

    def node_texture_get(self, inputName):
        if not self.use_nodes or self.node_principled_bsdf is None:
            return None
        return node_shader_utils.ShaderImageTextureWrapper(
            self, self.node_principled_bsdf,
            self.node_principled_bsdf.inputs[inputName],
            grid_row_diff=1,
        )


    # --------------------------------------------------------------------
    # Diffuse Texture.

    def diffuse_texture_get(self):
        return self.node_texture_get("Diffuse")

    diffuse_texture = property(diffuse_texture_get)


    # --------------------------------------------------------------------
    # Light Map.

    def lightmap_texture_get(self):
        return self.node_texture_get("Lightmap")

    lightmap_texture = property(lightmap_texture_get)


    # --------------------------------------------------------------------
    # Specular.

    def specular_texture_get(self):
        return self.node_texture_get("Specular")

    specular_texture = property(specular_texture_get)


    # --------------------------------------------------------------------
    # Emission texture.

    def emission_texture_get(self):
        return self.node_texture_get("Emission")

    emission_texture = property(emission_texture_get)


    # --------------------------------------------------------------------
    # Normal map.

    def normalmap_texture_get(self):
        return self.node_texture_get("Bump Map")

    normalmap_texture = property(normalmap_texture_get)


    # --------------------------------------------------------------------
    # Normal Mask.

    def normal_mask_texture_get(self):
        return self.node_texture_get("Bump Mask")

    normal_mask_texture = property(normal_mask_texture_get)


    # --------------------------------------------------------------------
    # Micro Bump 1.

    def microbump1_texture_get(self):
        return self.node_texture_get("MicroBump 1")

    microbump1_texture = property(microbump1_texture_get)


    # --------------------------------------------------------------------
    # Micro Bump 2.

    def microbump2_texture_get(self):
        return self.node_texture_get("MicroBump 2")

    microbump2_texture = property(microbump2_texture_get)


    # --------------------------------------------------------------------
    # Environmetn

    def environment_texture_get(self):
        return self.node_texture_get("Environment")

    environment_texture = property(environment_texture_get)




def test():
    if __name__ == "__main__":
        x= bpy.data.texts['x.py'].as_module()
        mat = bpy.context.active_object.material_slots[0].material
        xx = x.XPSShaderWrapper(mat)

        #print(type(XPSShaderWrapper(mat)))

    def getWrapper():
        x= bpy.data.texts['x.py'].as_module()
        mat = bpy.context.active_object.material_slots[0].material
        return x.XPSShaderWrapper(mat)




    from bpy_extras import io_utils, node_shader_utils
    mat = bpy.context.active_object.material_slots[0].material

    #wrap = node_shader_utils.PrincipledBSDFWrapper(mat)
    #print(wrap.node_principled_bsdf)


    #wrap = getWrapper()
    def xxxx():
        x= bpy.data.texts['x.py'].as_module()
        mat = bpy.context.active_object.material_slots[0].material
        z = x.XPSShaderWrapper(mat)

        mat = bpy.context.active_object.material_slots[0].material
        mat_wrap = node_shader_utils.PrincipledBSDFWrapper(mat) if mat else None


