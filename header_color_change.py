import bpy
from bpy.app.handlers import persistent

bl_info = {
	"name" : "header_color_change",
	"author" : "Bookyakuno",
	"version" : (1, 0, 0),
	"blender" : (2, 80, 0),
	"location" : "UI",
	"description" : "If the automatic keyframe feature is enabled, turn the header color red",
	"category" : "UI"
}

@persistent
def LoadPost_header_col(scn):
    """
    Sets the header column.

    Args:
        scn: (todo): write your description
    """
    handle_handlers_draw_header_col()

def handle_handlers_draw_header_col():
    """
    Handle the error handlers for the given handlers.

    Args:
    """
	if TEST_prefset not in bpy.app.handlers.depsgraph_update_post:
		bpy.app.handlers.depsgraph_update_post.append(TEST_prefset)


def TEST_prefset(scene):
    """
    Assigns prefset

    Args:
        scene: (todo): write your description
    """
    prefs = bpy.context.preferences

    if scene.tool_settings.use_keyframe_insert_auto == True:
        prefs.themes[0].topbar.space.header = (0.4, 0.000000, 0.000000, 1.000000)

    else:
        prefs.themes[0].topbar.space.header = (0.137255, 0.137255, 0.137255, 1.000000)


def register():
    """
    Registers the application.

    Args:
    """
	bpy.app.handlers.load_post.append(LoadPost_header_col)

def unregister():
    """
    Unregister the registered application.

    Args:
    """
	bpy.app.handlers.load_post.remove(LoadPost_header_col)


if __name__ == "__main__":
	register()
