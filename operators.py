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
import os
from bpy.types import Operator
from .functions import *


class WSM_OT_save_workspace(Operator):
    bl_idname = "wsm.save_workspace"
    bl_label = "Save Workspace"
    bl_description = "Save workspace data"

    name: bpy.props.StringProperty(name="Name")
    overwrite_existing: bpy.props.BoolProperty(
        name="Overwrite"
    )
    workspaces: bpy.props.EnumProperty(
        name="Workspaces",
        items=workspaces_enum,
        default=0
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        # col.use_property_split = True
        row = col.row(align=True)
        row.enabled = not self.overwrite_existing
        row.prop(self, "name")
        row = col.row(align=True)
        row.prop(self, "overwrite_existing")
        subrow = row.row(align=True)
        subrow.enabled = self.overwrite_existing
        subrow.prop(self, "workspaces", text='')

    def invoke(self, context, event):
        self.name = context.workspace.name
        return context.window_manager.invoke_props_dialog(self, width=250)

    def execute(self, context):
        active_name = context.workspace.name
        workspace_data = bpy.data.workspaces.get(active_name)
        if not workspace_data:
            return {'FINISHED'}
        data = [bpy.data.workspaces[active_name]]
        ws_name = self.name
        if self.overwrite_existing:
            workspace_data.name = self.workspaces
            ws_name = self.workspaces
        else:
            workspace_data.name = self.name
        filepath = os.path.join(get_config_path(), ws_name + ".blend")
        save_data_to_file(data, filepath, relative_path_remap=True)
        workspace_data.name = active_name

        msg = f"The {active_name} workspace has been saved to {filepath}."
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class WSM_OT_load_workspace(Operator):
    bl_idname = "wsm.load_workspace"
    bl_label = "Load Workspace"
    bl_description = "Load workspace data"
    bl_options = {'UNDO'}

    name: bpy.props.StringProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        filepath = os.path.join(get_config_path(), self.name + ".blend")
        if not os.path.isfile(filepath):
            return {'FINISHED'}
        ws = bpy.data.workspaces.get(self.name)
        is_exists = self.name in bpy.data.workspaces
        if prefs.duplicates == 'OVERWRITE':
            if context.window.workspace == ws:
                bpy.ops.workspace.delete()
                if ws:
                    ws.name += '_@#TEMP#@'
            elif is_exists:
                if ws:
                    delete_workspace_screens(self.name)
                bpy.data.batch_remove(ids=(ws,))
        workspace = append_data_from_a_file(filepath, self.name, prefs.duplicates)
        if workspace:
            context.window.workspace = bpy.data.workspaces[workspace]
        if prefs.duplicates == 'SKIP' and is_exists:
            return {'FINISHED'}
        msg = f"The {self.name} workspace has been loaded."
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class WSM_OT_remove_workspace(Operator):
    bl_idname = "wsm.remove_workspace"
    bl_label = "Remove Workspace"
    bl_description = "Delete workspace data file"

    name: bpy.props.StringProperty()

    def execute(self, context):
        filepath = os.path.join(get_config_path(), self.name + ".blend")
        if not os.path.isfile(filepath):
            return {'FINISHED'}
        os.remove(filepath)
        msg = f"The {self.name} workspace has been removed."
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class WSM_OT_clear_rest_workspaces(Operator):
    bl_idname = "wsm.clear_rest_workspaces"
    bl_label = "Clear Rest Tabs"
    bl_description = "Delete all workspace tabs except active"

    def execute(self, context):
        active_ws = context.workspace
        workspaces = [w for w in bpy.data.workspaces if w != active_ws]
        for ws in workspaces:
            delete_workspace_screens(ws.name, temp=False)
        bpy.data.batch_remove(ids=workspaces)
        return {'FINISHED'}


class WSM_OT_browse_config_folder(Operator):
    bl_idname = "wsm.browse_config_folder"
    bl_label = "Browse..."
    bl_description = "Open the config folder in the file browser containing saved workspace files"

    def execute(self, context):
        import sys
        directory = get_config_path()

        if sys.platform == "win32":
            os.startfile(directory)
        else:
            if sys.platform == "darwin":
                command = "open"
            else:
                command = "xdg-open"
            subprocess.call([command, directory])

        return {'FINISHED'}


classes = [
    WSM_OT_save_workspace,
    WSM_OT_load_workspace,
    WSM_OT_remove_workspace,
    WSM_OT_clear_rest_workspaces,
    WSM_OT_browse_config_folder,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
