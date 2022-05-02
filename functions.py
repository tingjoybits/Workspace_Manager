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


def validate_path(path):
    if not os.path.isdir(path):
        os.mkdir(path, mode=0o777)


def get_config_path(package_name=None):
    if not package_name:
        package_name = __package__.lower()
    user_path = bpy.utils.resource_path('USER')
    config_path = os.path.join(user_path, "config")
    config_path = os.path.join(config_path, package_name)
    validate_path(config_path)
    return config_path


def save_data_to_file(data, filepath, relative_path_remap=False):
    data_blocks = {
        *data,
        *bpy.data.node_groups
    }
    path_remap = 'NONE'
    if relative_path_remap:
        path_remap = 'RELATIVE_ALL'

    bpy.data.libraries.write(
        filepath, data_blocks, fake_user=True, path_remap=path_remap)
    return None


def get_file_list_names(path, full_name=False, extension='.json'):
    file_names = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and\
                file.lower().endswith(extension):
            if full_name:
                file_names.append(file)
                continue
            name = file.split(extension)[0]
            file_names.append(name)
    return file_names


def workspaces_enum(self, context):
    file_names = get_file_list_names(get_config_path(), full_name=False, extension='.blend')
    return [(n, n, "") for n in file_names]


def delete_workspace_screens(name, temp=False):
    if temp:
        workspace = bpy.data.workspaces.get(name + '_@#TEMP#@')
    else:
        workspace = bpy.data.workspaces.get(name)
    if workspace:
        screens = []
        for s in workspace.screens:
            s.name += '_@#TEMP#@'
            screens.append(s)
        bpy.data.batch_remove(ids=screens)


def append_data_from_a_file(filepath, name, duplicates='SKIP'):
    workspace = None
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        for w in data_from.workspaces:
            if w != name:
                continue
            if duplicates == 'SKIP' and w not in bpy.data.workspaces:
                data_to.workspaces.append(w)
            if duplicates == 'OVERWRITE':
                delete_workspace_screens(name, temp=True)
                data_to.workspaces.append(w)
            if duplicates == 'RENAME':
                workspace = w
                while workspace in bpy.data.workspaces:
                    workspace = get_name_copy(workspace)
                data_to.workspaces.append(w)
                return workspace
            workspace = w
    return workspace


def get_name_copy(name):
    try:
        if name[-4] == '.' and name[-1].isdecimal():
            return name[:-3] + str(int(name[-3:]) + 1).zfill(3)
    except IndexError:
        pass
    return name + '.' + str(1).zfill(3)
