
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


# CREATE NEW
class MaskModSmooth(bpy.types.Operator):
	'''Mask Smooth Surface'''
	bl_idname = "mesh.maskmod_smooth"
	bl_label = "Mask Smooth Surface"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod

	def poll(cls, context):
     """
     Poll for active mode.

     Args:
         cls: (todo): write your description
         context: (dict): write your description
     """

		return context.active_object is not None and context.active_object.mode == 'SCULPT'

	bpy.types.Scene.maskmod_smooth_strength = bpy.props.IntProperty(name = "Smooth strength", default = 10, min=-100, max=100)

	def execute(self, context):
     """
     Execute a list of the context represents.

     Args:
         self: (todo): write your description
         context: (dict): write your description
     """
		maskmod_smooth_strength = context.scene.maskmod_smooth_strength # update property from user input


		dynatopoEnabled = False

		if context.active_object.mode == 'SCULPT' :

			bpy.ops.mesh.masktovgroup()
			bpy.ops.mesh.masktovgroup_append()
			bpy.ops.sculpt.sculptmode_toggle()
			bpy.ops.object.modifier_add(type='SMOOTH')
			bpy.context.object.modifiers["Smooth"].iterations = maskmod_smooth_strength
			bpy.context.object.modifiers["Smooth"].vertex_group = "Mask"
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")

			bpy.ops.sculpt.sculptmode_toggle()
			# bpy.ops.mesh.vgrouptomask_append()
			bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)


		if dynatopoEnabled :
			bpy.ops.sculpt.dynamic_topology_toggle()
		return {'FINISHED'}

# CREATE NEW
class MaskModDisplace(bpy.types.Operator):
	'''Mask Smooth Surface'''
	bl_idname = "mesh.maskmod_displace"
	bl_label = "Mask Displace Surface"
	bl_options = {'REGISTER', 'UNDO'}




	@classmethod

	def poll(cls, context):
     """
     Poll for active mode.

     Args:
         cls: (todo): write your description
         context: (dict): write your description
     """

		return context.active_object is not None and context.active_object.mode == 'SCULPT'

	bpy.types.Scene.maskmod_displace_strength = bpy.props.FloatProperty(name = "Displace strength", default = 0.2, min=-100, max=100)
	bpy.types.Scene.maskmod_displace_apply = bpy.props.BoolProperty(name = "Displace Apply", default = True)

	# bpy.types.Scene.maskmod_displace_apply: bpy.props.BoolProperty(
	# name="maskmod_displace_apply",
	# default=True,
	# description="maskmod_displace_apply"
	# )



	def execute(self, context):
     """
     Execute the operations that mask.

     Args:
         self: (todo): write your description
         context: (dict): write your description
     """
		maskmod_displace_strength = context.scene.maskmod_displace_strength # update property from user input
		maskmod_displace_apply = context.scene.maskmod_displace_apply # update property from user input


		dynatopoEnabled = False

		if context.active_object.mode == 'SCULPT' :

			bpy.ops.mesh.masktovgroup()
			bpy.ops.mesh.masktovgroup_append()
			bpy.ops.sculpt.sculptmode_toggle()
			bpy.ops.object.modifier_add(type='DISPLACE')
			# bpy.context.object.modifiers["Displace"].name = "Displace_mask"

			bpy.context.object.modifiers["Displace"].strength = maskmod_displace_strength
			bpy.context.object.modifiers["Displace"].vertex_group = "Mask"
			if maskmod_displace_apply == True:
				bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
				bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)

			bpy.ops.sculpt.sculptmode_toggle()
			# bpy.ops.mesh.vgrouptomask_append()


		if dynatopoEnabled :
			bpy.ops.sculpt.dynamic_topology_toggle()
		return {'FINISHED'}






	# @classmethod
	#
	# def poll(cls, context):
	#
	# 	return context.active_object is not None and context.active_object.mode == 'SCULPT'
	#
	# bpy.types.Scene.maskmod_displace_strength = bpy.props.FloatProperty(name = "Displace strength", default = 0.2, min=-100, max=100)
	# bpy.types.Scene.maskmod_displace_apply = bpy.props.BoolProperty(name = "Displace Apply", default = True)
	#
	# def execute(self, context):
	# 	maskmod_displace_strength = context.scene.maskmod_displace_strength # update property from user input
	# 	maskmod_displace_apply = context.scene.maskmod_displace_apply # update property from user input
	#
	#
	# 	dynatopoEnabled = False
	#
	# 	if context.active_object.mode == 'SCULPT' :
	# 		bpy.ops.sculpt.sculptmode_toggle()
	# 		# DISPLACE
	# 		bpy.ops.object.modifier_add(type='DISPLACE')
	# 		bpy.context.object.modifiers["Displace"].vertex_group = "Mask"
	# 		bpy.context.object.modifiers["Displace"].strength = maskmod_displace_strength
	# 		# DISPLACE end
	#
	# 		bpy.ops.sculpt.sculptmode_toggle()
	# 		bpy.ops.mesh.masktovgroup()
	# 		bpy.ops.mesh.masktovgroup_append()
	#
	# 		if bpy.types.Scene.maskmod_displace_apply == True:
	# 			bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
	# 		bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)
	#
	#
	# 	if dynatopoEnabled :
	# 		bpy.ops.sculpt.dynamic_topology_toggle()
	# 	return {'FINISHED'}
	#





def register():
    """
    Registers a mask.

    Args:
    """

    bpy.types.Scene.maskmod_smooth_strength = MaskModSmooth.maskmod_smooth_strength
    bpy.types.Scene.maskmod_displace_strength = MaskModDisplace.maskmod_displace_strength
    bpy.types.Scene.maskmod_displace_apply = MaskModDisplace.maskmod_displace_apply

    bpy.utils.register_module(__name__)


def unregister():
    """
    Unregister a mask.

    Args:
    """

    bpy.types.Scene.maskmod_smooth_strength
    bpy.types.Scene.maskmod_displace_strength
    bpy.types.Scene.maskmod_displace_apply

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
