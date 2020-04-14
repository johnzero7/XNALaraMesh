import bpy
from bpy_extras import node_shader_utils
from mathutils import Vector


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
            # print("loop:",n.name)
            if n.bl_idname == 'ShaderNodeOutputMaterial' and n.inputs[0].is_linked:
                # print("output found:")
                node_out = n
                node_principled = n.inputs[0].links[0].from_node
            elif n.bl_idname == 'ShaderNodeGroup' and n.node_tree.name == 'XPS Shader' and n.outputs[0].is_linked:
                # print("xps shader found")
                node_principled = n
                for lnk in n.outputs[0].links:
                    node_out = lnk.to_node
                    if node_out.bl_idname == 'ShaderNodeOutputMaterial':
                        break
            if (
                node_out is not None and node_principled is not None
                and node_out.bl_idname == 'ShaderNodeOutputMaterial'
                and node_principled.bl_idname == 'ShaderNodeGroup'
                and node_principled.node_tree.name == 'XPS Shader'
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
    # Get Image wrapper.

    def node_texture_get(self, inputName):
        if not self.use_nodes or self.node_principled_bsdf is None:
            return None
        return node_shader_utils.ShaderImageTextureWrapper(
            self, self.node_principled_bsdf,
            self.node_principled_bsdf.inputs[inputName],
            grid_row_diff=1,
        )

    # --------------------------------------------------------------------
    # Get Environment wrapper.

    def node_environment_get(self, inputName):
        if not self.use_nodes or self.node_principled_bsdf is None:
            return None
        return ShaderEnvironmentTextureWrapper(
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
    # Environment

    def environment_texture_get(self):
        return self.node_environment_get("Environment")

    environment_texture = property(environment_texture_get)


class ShaderEnvironmentTextureWrapper():
    """
    Generic 'environment texture'-like wrapper, handling image node
    """

    # Note: this class assumes we are using nodes, otherwise it should never be used...

    NODES_LIST = (
        "node_dst",
        "socket_dst",

        "_node_image",
        "_node_mapping",
    )

    __slots__ = (
        "owner_shader",
        "is_readonly",
        "grid_row_diff",
        "use_alpha",
        "colorspace_is_data",
        "colorspace_name",
        *NODES_LIST,
    )

    def __new__(cls, owner_shader: node_shader_utils.ShaderWrapper, node_dst, socket_dst, *_args, **_kwargs):
        instance = owner_shader._textures.get((node_dst, socket_dst), None)
        if instance is not None:
            return instance
        instance = super(ShaderEnvironmentTextureWrapper, cls).__new__(cls)
        owner_shader._textures[(node_dst, socket_dst)] = instance
        return instance

    def __init__(self, owner_shader: node_shader_utils.ShaderWrapper, node_dst, socket_dst, grid_row_diff=0,
                 use_alpha=False, colorspace_is_data=..., colorspace_name=...):
        self.owner_shader = owner_shader
        self.is_readonly = owner_shader.is_readonly
        self.node_dst = node_dst
        self.socket_dst = socket_dst
        self.grid_row_diff = grid_row_diff
        self.use_alpha = use_alpha
        self.colorspace_is_data = colorspace_is_data
        self.colorspace_name = colorspace_name

        self._node_image = ...
        self._node_mapping = ...

        # tree = node_dst.id_data
        # nodes = tree.nodes
        # links = tree.links

        if socket_dst.is_linked:
            from_node = socket_dst.links[0].from_node
            if from_node.bl_idname == 'ShaderNodeTexEnvironment':
                self._node_image = from_node

        if self.node_image is not None:
            socket_dst = self.node_image.inputs["Vector"]
            if socket_dst.is_linked:
                from_node = socket_dst.links[0].from_node
                if from_node.bl_idname == 'ShaderNodeMapping':
                    self._node_mapping = from_node

    def copy_from(self, tex):
        # Avoid generating any node in source texture.
        is_readonly_back = tex.is_readonly
        tex.is_readonly = True

        if tex.node_image is not None:
            self.image = tex.image
            self.projection = tex.projection
            self.texcoords = tex.texcoords
            self.copy_mapping_from(tex)

        tex.is_readonly = is_readonly_back

    def copy_mapping_from(self, tex):
        # Avoid generating any node in source texture.
        is_readonly_back = tex.is_readonly
        tex.is_readonly = True

        if tex.node_mapping is None:  # Used to actually remove mapping node.
            if self.has_mapping_node():
                # We assume node_image can never be None in that case...
                # Find potential existing link into image's Vector input.
                socket_dst = socket_src = None
                if self.node_mapping.inputs["Vector"].is_linked:
                    socket_dst = self.node_image.inputs["Vector"]
                    socket_src = self.node_mapping.inputs["Vector"].links[0].from_socket

                tree = self.owner_shader.material.node_tree
                tree.nodes.remove(self.node_mapping)
                self._node_mapping = None

                # If previously existing, re-link texcoords -> image
                if socket_src is not None:
                    tree.links.new(socket_src, socket_dst)
        elif self.node_mapping is not None:
            self.translation = tex.translation
            self.rotation = tex.rotation
            self.scale = tex.scale

        tex.is_readonly = is_readonly_back

    # --------------------------------------------------------------------
    # Image.

    def node_image_get(self):
        if self._node_image is ...:
            # Running only once, trying to find a valid image node.
            if self.socket_dst.is_linked:
                node_image = self.socket_dst.links[0].from_node
                if node_image.bl_idname == 'ShaderNodeTexImage':
                    self._node_image = node_image
                    self.owner_shader._grid_to_location(0, 0, ref_node=node_image)
            if self._node_image is ...:
                self._node_image = None
        if self._node_image is None and not self.is_readonly:
            tree = self.owner_shader.material.node_tree

            node_image = tree.nodes.new(type='ShaderNodeTexImage')
            self.owner_shader._grid_to_location(-1, 0 + self.grid_row_diff, dst_node=node_image, ref_node=self.node_dst)

            tree.links.new(node_image.outputs["Alpha" if self.use_alpha else "Color"], self.socket_dst)

            self._node_image = node_image
        return self._node_image

    node_image = property(node_image_get)

    def image_get(self):
        return self.node_image.image if self.node_image is not None else None

    @node_shader_utils._set_check
    def image_set(self, image):
        if self.colorspace_is_data is not ...:
            if image.colorspace_settings.is_data != self.colorspace_is_data and image.users >= 1:
                image = image.copy()
            image.colorspace_settings.is_data = self.colorspace_is_data
        if self.colorspace_name is not ...:
            if image.colorspace_settings.is_data != self.colorspace_is_data and image.users >= 1:
                image = image.copy()
            image.colorspace_settings.name = self.colorspace_name
        self.node_image.image = image

    image = property(image_get, image_set)

    def projection_get(self):
        return self.node_image.projection if self.node_image is not None else 'EQUIRECTANGULAR'

    @node_shader_utils._set_check
    def projection_set(self, projection):
        self.node_image.projection = projection

    projection = property(projection_get, projection_set)

    def texcoords_get(self):
        if self.node_image is not None:
            socket = (self.node_mapping if self.has_mapping_node() else self.node_image).inputs["Vector"]
            if socket.is_linked:
                return socket.links[0].from_socket.name
        return 'UV'

    @node_shader_utils._set_check
    def texcoords_set(self, texcoords):
        # Image texture node already defaults to UVs, no extra node needed.
        # ONLY in case we do not have any texcoords mapping!!!
        if texcoords == 'UV' and not self.has_mapping_node():
            return
        tree = self.node_image.id_data
        links = tree.links
        node_dst = self.node_mapping if self.has_mapping_node() else self.node_image
        socket_src = self.owner_shader.node_texcoords.outputs[texcoords]
        links.new(socket_src, node_dst.inputs["Vector"])

    texcoords = property(texcoords_get, texcoords_set)

    # --------------------------------------------------------------------
    # Mapping.

    def has_mapping_node(self):
        return self._node_mapping not in {None, ...}

    def node_mapping_get(self):
        if self._node_mapping is ...:
            # Running only once, trying to find a valid mapping node.
            if self.node_image is None:
                return None
            if self.node_image.inputs["Vector"].is_linked:
                node_mapping = self.node_image.inputs["Vector"].links[0].from_node
                if node_mapping.bl_idname == 'ShaderNodeMapping':
                    self._node_mapping = node_mapping
                    self.owner_shader._grid_to_location(0, 0 + self.grid_row_diff, ref_node=node_mapping)
            if self._node_mapping is ...:
                self._node_mapping = None
        if self._node_mapping is None and not self.is_readonly:
            # Find potential existing link into image's Vector input.
            socket_dst = self.node_image.inputs["Vector"]
            # If not already existing, we need to create texcoords -> mapping link (from UV).
            socket_src = (
                socket_dst.links[0].from_socket if socket_dst.is_linked
                else self.owner_shader.node_texcoords.outputs['UV']
            )

            tree = self.owner_shader.material.node_tree
            node_mapping = tree.nodes.new(type='ShaderNodeMapping')
            node_mapping.vector_type = 'TEXTURE'
            self.owner_shader._grid_to_location(-1, 0, dst_node=node_mapping, ref_node=self.node_image)

            # Link mapping -> image node.
            tree.links.new(node_mapping.outputs["Vector"], socket_dst)
            # Link texcoords -> mapping.
            tree.links.new(socket_src, node_mapping.inputs["Vector"])

            self._node_mapping = node_mapping
        return self._node_mapping

    node_mapping = property(node_mapping_get)

    def translation_get(self):
        if self.node_mapping is None:
            return Vector((0.0, 0.0, 0.0))
        return self.node_mapping.inputs['Location'].default_value

    @node_shader_utils._set_check
    def translation_set(self, translation):
        self.node_mapping.inputs['Location'].default_value = translation

    translation = property(translation_get, translation_set)

    def rotation_get(self):
        if self.node_mapping is None:
            return Vector((0.0, 0.0, 0.0))
        return self.node_mapping.inputs['Rotation'].default_value

    @node_shader_utils._set_check
    def rotation_set(self, rotation):
        self.node_mapping.inputs['Rotation'].default_value = rotation

    rotation = property(rotation_get, rotation_set)

    def scale_get(self):
        if self.node_mapping is None:
            return Vector((1.0, 1.0, 1.0))
        return self.node_mapping.inputs['Scale'].default_value

    @node_shader_utils._set_check
    def scale_set(self, scale):
        self.node_mapping.inputs['Scale'].default_value = scale

    scale = property(scale_get, scale_set)
