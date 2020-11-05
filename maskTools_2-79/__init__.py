bl_info = {
	"name": "Mask Tools",
	"author": "Stanislav Blinov,Yigit Savtur,Bookyakuno (2.8Update)",
	"version": (0, 37,0),
	"blender": (2, 79,0),
	"location": "3d View > Tool shelf (T) > Sculpt",
	"description": "Tools for Converting Sculpt Masks to Vertex groups",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Sculpt"}



import bpy

from .maskToVGroup import *
from .vgroupToMask import *
from .maskFromCavity import *
from .maskToAction import *




from mathutils import Vector

import bmesh
import bpy
import collections
import mathutils
import math
from bpy_extras import view3d_utils
from bpy.types import (
		Operator,
		Menu,
		Panel,
		PropertyGroup,
		AddonPreferences,
		)
from bpy.props import (
		BoolProperty,
		EnumProperty,
		FloatProperty,
		IntProperty,
		PointerProperty,
		StringProperty,
		)






class MASKTOOLS_AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	def draw(self, context):
     """
     Draw the layout

     Args:
         self: (todo): write your description
         context: (dict): write your description
     """
		layout = self.layout

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Deselect", icon='MOD_MASK')
		row.label(text="LEFT MOUSE   : DoubleClick + Ctrl + Shift",icon="MOUSE_LMB")

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Invert", icon='PIVOT_MEDIAN')
		row.label(text="RIGHT MOUSE : DoubleClick + Ctrl + Shift",icon="MOUSE_RMB")

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Invert", icon='PIVOT_MEDIAN')
		row.label(text="LEFT MOUSE   : DoubleClick + Ctrl + alt",icon="MOUSE_LMB")

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Smooth", icon='MOD_SMOOTH')
		row.label(text="LEFT MOUSE   : DoubleClick + Shift",icon="MOUSE_LMB")

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Sharp", icon='IMAGE_ALPHA')
		row.label(text="RIGHT MOUSE : DoubleClick + Shift",icon="MOUSE_RMB")

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Fat", icon='ZOOMIN')
		row.label(text="LEFT MOUSE   : DoubleClick + Alt",icon="MOUSE_LMB")

		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Less", icon='ZOOMOUT')
		row.label(text="RIGHT MOUSE : DoubleClick + Alt",icon="MOUSE_RMB")
		col = layout.column(align=True)
		row = col.row(align=True)
		row.label(text="– Remove", icon='X')
		row.label(text="BACKSPACE")



	def execute(self,context):
     """
     Execute the context.

     Args:
         self: (todo): write your description
         context: (dict): write your description
     """
		return {'FINISHED'}





class MaskToolsPanel(Panel):
	"""Creates a Mask Tool Box in the Viewport Tool Panel"""
	# bl_category = "Sculpt"
	# bl_idname = "MESH_OT_masktools"
	# bl_space_type = 'VIEW_3D'
	# bl_region_type = 'UI'
	# bl_label = "Mask Tools"
	bl_category = "Sculpt"
	bl_label = "Mask Tools"
	bl_idname = "MESH_OT_masktools"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'



	def draw(self, context):
     """
     Draw the layout

     Args:
         self: (todo): write your description
         context: (dict): write your description
     """
		layout = self.layout

		###############################################################
		row = layout.row(align = True)
		row.label(text = "Vertex Group :", icon = 'GROUP_VERTEX')
		row = layout.row(align = True)
		row.label(text = "Save Mask to VGroup")

		row = layout.row()
		row.scale_y = 1.3
		row.operator("mesh.masktovgroup", text = "Create VGroup", icon = 'GROUP_VERTEX')
		row = layout.row(align = True)
		row.operator("mesh.masktovgroup_append", text = "Add VGroup", icon = 'EXPORT')
		row.operator("mesh.masktovgroup_remove", text = "Difference VGroup", icon = 'UNLINKED')

		space = layout.row()

		###############################################################
		row = layout.row(align = True)
		row.label(text = "Mask :", icon = 'MOD_MASK')
		row = layout.row(align = True)
		row.label(text = "Import VGroup to Mask ")



		row = layout.row(align = True)
		row.scale_y = 1.3
		row.operator("mesh.vgrouptomask_append", text = "Add", icon = 'IMPORT')
		row.operator("mesh.vgrouptomask_remove", text = "Difference", icon = 'UNLINKED')
		row = layout.row()
		row.operator("mesh.vgrouptomask", text = "New Mask", icon='NONE')

		space = layout.row()

		row = layout.row(align = True)
		row.label(text = "Mask Smooth/Sharp :", icon = 'MOD_SMOOTH')

		row = layout.row(align = True)
		# row.label(text = "Mask Smooth", icon = 'MOD_MASK')
		row.scale_y = 1.3
		row.operator("mesh.mask_smooth_all", text = "Smooth", icon = 'SMOOTH')
		row.operator("mesh.mask_sharp", text = "Sharp", icon = 'IMAGE_ALPHA')

		row = layout.row(align = False)
		row.prop(bpy.context.scene,"mask_smooth_strength", text = "Mask Smooth Strength", icon='MOD_MASK',slider = True)


		space = layout.row()



		###############################################################
		row = layout.row(align = True)
		row.label(text = "Mask Fat/Less :", icon = 'ZOOMIN')
		row = layout.row(align = True)
		row.scale_y = 1.3
		row.operator("mesh.mask_fat", text = "Mask Fat", icon = 'ZOOMIN')
		row.operator("mesh.mask_less", text = "Mask Less", icon = 'ZOOMOUT')

		row = layout.row(align = True)
		row.prop(bpy.context.scene,"mask_fat_repeat", text = "Mask Fat Repeat", icon='MOD_MASK',slider = True)
		row.prop(bpy.context.scene,"mask_less_repeat", text = "Mask Less Repeat", icon='MOD_MASK',slider = True)

		space = layout.row()

		###############################################################
		row = layout.row(align = True)
		row.label(text = "Mask Edge/Cavity :", icon = 'EDGESEL')


		row = layout.row(align = True)
		# row.label(text = "Mask by Edges :", icon = 'MOD_MASK')
		row.scale_y = 1.3
		row.operator("mesh.mask_from_edges", text = "Mask by Edges", icon = 'EDGESEL')

		row = layout.row(align = True)
		row.prop(bpy.context.scene,"mask_edge_angle", text = "Edge Angle",icon='MOD_MASK',slider = True)
		row.prop(bpy.context.scene,"mask_edge_strength", text = "Mask Strength", icon='MOD_MASK',slider = True)

		space = layout.row()
		space = layout.row()

		row = layout.row(align = True)
		# row.label(text = "Mask by Cavity:", icon = 'MOD_MASK')
		row.scale_y = 1.3
		row.operator("mesh.mask_from_cavity", text = "Mask by Cavity", icon = 'STYLUS_PRESSURE')

		row = layout.row(align = True)
		row.prop(bpy.context.scene,"mask_cavity_angle", text = "Cavity Angle",icon='MOD_MASK',slider = True)
		row.prop(bpy.context.scene,"mask_cavity_strength", text = "Mask Strength", icon='MOD_MASK',slider = True)

		space = layout.row()
		space = layout.row()



		###############################################################
		row = layout.row(align = True)
		row.label(text = "Mask Misc :", icon = 'FORCE_VORTEX')

		space = layout.row()
		row = layout.row(align = True)
		row.operator("mesh.mask_sharp_thick", text = "Mask Sharp (Thick)", icon = 'NONE')
		row = layout.row(align = True)
		maskCavity = layout.row(align = False)
		maskCavity.prop(bpy.context.scene,"mask_sharp_thick", text = "Mask Sharp Thick Strength", icon='MOD_MASK',slider = True)

		space = layout.row()
		row = layout.row(align = True)
		row.operator("mesh.mask_duplicate", text = "Mask Duplicate")
		# space = layout.row()
		# row = layout.row(align = True)
		# row.operator("mesh.mask_lattice", text = "Mask Lattice")
		space = layout.row()
		row = layout.row(align = True)
		row.operator("mesh.mask_polygon_remove", text = "Mask Polygon Remove")




		space = layout.row()
		space = layout.row()
		space = layout.row()
		row = layout.row(align = True)
		row.operator("mesh.maskmod_displace", icon = 'MOD_DISPLACE')
		row = layout.row(align = True)
		row = layout.row(align = False)
		row.prop(bpy.context.scene,"maskmod_displace_apply", icon='MOD_MASK')
		row.prop(bpy.context.scene,"maskmod_displace_strength", icon='MOD_MASK',slider = True)

		space = layout.row()
		row = layout.row(align = True)
		row.operator("mesh.maskmod_smooth", icon = 'MOD_SMOOTH')
		row = layout.row(align = True)
		row = layout.row(align = False)
		row.prop(bpy.context.scene,"maskmod_smooth_strength", icon='MOD_MASK',slider = True)








classes = {
MASKTOOLS_AddonPreferences,
MaskToolsPanel,
# MASKTOOLS_OT_AddHotkey,

MaskToVertexGroup,
MaskToVertexGroupAppend,
MaskToVertexGroupRemove,

VertexGroupToMask,
VertexGroupToMaskAppend,
VertexGroupToMaskRemove,

MaskFromCavity,
MaskFromEdges,
MaskSmoothAll,
MaskFat,
MaskLess,
MaskSharp,
MaskSharpThick,
MaskLattice,
MaskDuplicate,
MaskArmture,
MaskPolygonRemove,


MaskModSmooth,
MaskModDisplace,
}

addon_keymaps = []




################################################################
# # # # # # # # プロパティの指定に必要なもの
def kmi_props_setattr(kmi_props, attr, value):
    """
    Set kmi_props_props

    Args:
        kmi_props: (todo): write your description
        attr: (str): write your description
        value: (todo): write your description
    """
	try:
		setattr(kmi_props, attr, value)
	except AttributeError:
		print("Warning: property '%s' not found in keymap item '%s'" %
			  (attr, kmi_props.__class__.__name__))
	except Exception as e:
		print("Warning: %r" % e)

################################################################




def register():
    """
    Register kmi classes

    Args:
    """

	for cls in classes:
		bpy.utils.register_class(cls)





	wm = bpy.context.window_manager
	#kc = wm.keyconfigs.user      # for adding hotkeys independent from addon
	#km = kc.keymaps['Screen']
	kc = wm.keyconfigs.addon    # for hotkeys within an addon

	wm = bpy.context.window_manager
	keynew = wm.keyconfigs.addon.keymaps.new




	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('paint.mask_lasso_gesture', 'RIGHTMOUSE', 'PRESS',ctrl=True,shift=True)
	kmi_props_setattr(kmi.properties, 'mode','VALUE')
	kmi_props_setattr(kmi.properties, "value", 0.0)
	kmi.active = True
	addon_keymaps.append((km, kmi))

	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('paint.mask_lasso_gesture', 'LEFTMOUSE', 'PRESS',ctrl=True,shift=True)
	kmi_props_setattr(kmi.properties, 'mode','VALUE')
	kmi_props_setattr(kmi.properties, "value", 1.0)
	kmi.active = True
	addon_keymaps.append((km, kmi))


	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('paint.mask_flood_fill', 'RIGHTMOUSE', 'DOUBLE_CLICK', ctrl=True,shift=True)
	kmi_props_setattr(kmi.properties, "mode",'INVERT')
	kmi.active = True
	addon_keymaps.append((km, kmi))
	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('paint.mask_flood_fill', 'LEFTMOUSE', 'DOUBLE_CLICK', ctrl=True,alt=True)
	kmi_props_setattr(kmi.properties, "mode",'INVERT')
	kmi.active = True
	addon_keymaps.append((km, kmi))


	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('paint.mask_flood_fill', 'LEFTMOUSE', 'DOUBLE_CLICK', ctrl=True,shift=True)
	kmi_props_setattr(kmi.properties, 'mode','VALUE')
	kmi_props_setattr(kmi.properties, "value", 0.0)
	kmi.active = True
	addon_keymaps.append((km, kmi))


	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('mesh.mask_smooth_all', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)
	kmi.active = True
	addon_keymaps.append((km, kmi))
	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('mesh.mask_sharp', 'RIGHTMOUSE', 'DOUBLE_CLICK', shift=True)
	kmi.active = True
	addon_keymaps.append((km, kmi))

	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('mesh.mask_fat', 'LEFTMOUSE', 'DOUBLE_CLICK', alt=True)
	kmi.active = True
	addon_keymaps.append((km, kmi))
	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('mesh.mask_less', 'RIGHTMOUSE', 'DOUBLE_CLICK', alt=True)
	kmi.active = True
	addon_keymaps.append((km, kmi))

	################################################################
	km = keynew('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
	kmi = km.keymap_items.new('mesh.mask_polygon_remove', 'BACK_SPACE', 'PRESS')
	kmi.active = True
	addon_keymaps.append((km, kmi))









	# add_hotkey()

def unregister():
    """
    Removes all addon from the registry.

    Args:
    """
	for cls in classes:
		bpy.utils.unregister_class(cls)

	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()
	# remove_hotkey()


if __name__ == "__main__":
	register()
