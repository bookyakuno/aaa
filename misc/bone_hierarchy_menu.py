import bpy


# ボーンを階層表示するメニュー
def bone_hierarchy_menu(self,context,layout):
    """
    Make a hierarchy layout.

    Args:
        self: (todo): write your description
        context: (todo): write your description
        layout: (str): write your description
    """
	if not bpy.context.active_object:
		return
	if not bpy.context.object.type == "ARMATURE":
		return

	obj = bpy.context.object
	bone_data = obj.data.bones

	col = layout.column(align=True)

	# ボーンの最上階層(親なし)
	top_bone_l = [b for b in bone_data if not b.parent]

	for bone in top_bone_l:
		# アクティブなボーンのアイコン
		try:
			if bone.name == bone_data.active.name:
				icon_val = "BONE_DATA"
			else:
				icon_val = "BLANK1"
		except: icon_val = "BLANK1"

		if not bone.parent and bone.children: # トップ
			col.prop(bone ,"name",text="top",icon=icon_val)

		if not bone.children: # 子がない(一番した)
			col.prop(bone ,"name",text="no child",icon=icon_val)
			continue

		# メイン
		bone_hierarchy_loop(obj,bone,col,icon_val,1)
		col.separator()


# ループ
def bone_hierarchy_loop(obj,bone,col,icon_val,count):
    """
    Returns a hierarchy. hier.

    Args:
        obj: (todo): write your description
        bone: (str): write your description
        col: (todo): write your description
        icon_val: (str): write your description
        count: (int): write your description
    """
	for bone in bone.children:
		bone_child_item_menu(obj,bone,col,icon_val,count)
		bone_hierarchy_loop(obj,bone,col,icon_val,count + 1)

	if not bone.children:
		return


# 各ボーンのメニュー
def bone_child_item_menu(obj,bone,col,icon_val,range_count):
    """
    Handle a single item menu.

    Args:
        obj: (todo): write your description
        bone: (todo): write your description
        col: (todo): write your description
        icon_val: (int): write your description
        range_count: (str): write your description
    """
	rows = col.row(align=True)
	for i in range(range_count):
		rows.separator(factor=2)
	rows.prop(bone ,"name",text="",icon=icon_val)
