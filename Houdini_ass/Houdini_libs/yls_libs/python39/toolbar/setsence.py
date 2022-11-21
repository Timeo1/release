import os
import hou
import getpass


def get_path():
    sel_path = hou.ui.readInput('Set sence',buttons=('Set', 'close'),default_choice=0, close_choice=1, title='Set Sence', initial_contents='copy your work path!')
    return sel_path

#todo
#if this hipFile exists Find the lastversion and up the version to save
def main():
    sel_path = get_path()
    if os.path.exists(sel_path[1]):
        sel = sel_path[0]
        if sel==0:
            work_path = sel_path[1]
            work_path_list = work_path.split(os.sep)
            project_name = work_path_list[2]
            shot = work_path_list[5]
            department = work_path_list[6].lower()
            version = 'v001.01'
            base_name = '_'.join([project_name, shot, department, version])
            base_name = base_name +'.hip'
            abs_path = os.path.join(work_path, base_name)
            hou.hipFile.setName(abs_path)
            hou.hipFile.save()

if __name__ == '__main__':
    main()