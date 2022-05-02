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
from bpy.types import AddonPreferences


class WSM_Preferences(AddonPreferences):
    bl_idname = __package__

    duplicates: bpy.props.EnumProperty(
        name="Duplicates",
        items=[
            ('OVERWRITE', 'Overwrite', 'Replace identical workspace names and remove the existing workspace data'),
            ('RENAME', 'Rename', 'Auto-rename workspaces with the same name'),
            ('SKIP', 'Skip', 'Do not change workspaces with the same name')
        ],
        default='OVERWRITE'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'duplicates')


classes = (
    WSM_Preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
