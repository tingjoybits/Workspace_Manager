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
import importlib
from . import ui, operators, functions, properties

bl_info = {
    "name": "Workspace Manager",
    "author": "TingJoyBits",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "Top bar header",
    "description": "Quickly save and load custom workspaces",
    "warning": "",
    "doc_url": "https://github.com/tingjoybits/Workspace_Manager",
    "category": "Interface",
}

modules = (
    functions,
    properties,
    operators,
    ui,
)


def register():
    for module in modules:
        importlib.reload(module)
        if hasattr(module, 'register'):
            module.register()


def unregister():
    for module in modules[::-1]:
        if hasattr(module, 'unregister'):
            module.unregister()


if __name__ == "__main__":
    register()
