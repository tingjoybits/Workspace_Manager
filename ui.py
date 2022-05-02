# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import Menu
from .functions import *


class WSM_MT_Workspace_Manager(Menu):
    bl_label = "Workspace Manager"
    bl_idname = "WSM_MT_Workspace_Manager_main_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wsm.save_workspace", icon='FILE_TICK')
        layout.separator()
        layout.label(text="Load:", icon='WORKSPACE')
        workspace_names = get_file_list_names(get_config_path(), full_name=False, extension='.blend')
        for n in workspace_names:
            layout.operator("wsm.load_workspace", text=n).name = n
        layout.separator()
        prefs = context.preferences.addons[__package__].preferences
        layout.label(text="Duplicates:")
        layout.prop(prefs, 'duplicates', text='')
        layout.separator()
        layout.menu("WSM_MT_remove_workspace_menu", icon='TRASH')
        layout.separator()
        layout.operator("wsm.browse_config_folder", icon='FILEBROWSER')
        layout.separator()
        layout.operator("wsm.clear_rest_workspaces")


class WSM_MT_Remove_Workspace_List(Menu):
    bl_label = "Remove"
    bl_idname = "WSM_MT_remove_workspace_menu"

    def draw(self, context):
        layout = self.layout
        workspace_names = get_file_list_names(get_config_path(), full_name=False, extension='.blend')
        for n in workspace_names:
            layout.operator("wsm.remove_workspace", text=n, icon='TRASH').name = n


def header_extension(self, context):
    region = context.region
    if region.alignment == 'RIGHT':
        self.layout.menu("WSM_MT_Workspace_Manager_main_menu", text="", icon='DESKTOP')


classes = [
    WSM_MT_Remove_Workspace_List,
    WSM_MT_Workspace_Manager,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_HT_upper_bar.prepend(header_extension)


def unregister():
    bpy.types.TOPBAR_HT_upper_bar.remove(header_extension)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
