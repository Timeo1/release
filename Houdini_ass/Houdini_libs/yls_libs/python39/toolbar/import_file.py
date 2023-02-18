# -*- coding: utf-8 -*-
# Author: yls
# date: 2021/03/16

import hou
import os
import re
def main():
    obj_dir_path = hou.ui.selectFile(title = 'Select_Folder', file_type = hou.fileType.Directory)
    char_len = len(obj_dir_path)
    if char_len > 1:    
        name = 'import_file'
        Loader = hou.node('/obj/').createNode('geo', name)
        obj_dir_path_expand = hou.expandString(obj_dir_path)
        obj_files_list = os.listdir(obj_dir_path_expand)
        obj_node_list = []

    if char_len > 1:
        for obj_file in obj_files_list:
            pattern = r'.*(\.abc)$'
            rx = re.compile(pattern)
            result = rx.match(obj_file)
            if(result!=None): 
                obj_node = Loader.createNode('alembic', obj_file)
                obj_node.parm('fileName').set(obj_dir_path + obj_file)
                obj_node_list.append(obj_node)

        
        Switch_node = Loader.createNode('merge', 'abc_merge')

        for node in obj_node_list:
            Switch_node.setNextInput(node)
        Switch_node.setDisplayFlag(True)
        Loader.layoutChildren()
        