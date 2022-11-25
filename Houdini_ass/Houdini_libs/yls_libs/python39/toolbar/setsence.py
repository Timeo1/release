import os
import hou
import re
import getpass
import importallabc


def set_path():
    sel_path = hou.ui.readInput('Set sence',buttons=('Set', 'close'),default_choice=0, close_choice=1, title='Set Sence', initial_contents='copy your work path!')
    return sel_path


class Sence():
    def __init__(self, filename, camera) -> None:
        self.filename = filename
        self.camera = camera
        self.FPS = 24
        self.Frame = (0, 100)
        
        

    def get_path(self):
        return self.set_path()[1]
    
    def get_select(self):
        return self.set_path()[0]

    def serach_project_name(self, path):
        pattern = re.compile(r'projects/\w+/')
        matched = pattern.match(path, re.I)
        return matched.group()
    
    def serach_shot_name(self, path):
        pattern = re.compile(r's\w+\d+/')
        matched = pattern.match(path, re.I)
        return matched.group()
    
    def serach_department_name(self, path):
        pattern = re.compile(r'{CFX | VFX}')
        matched = pattern.match(path, re.I)
        return matched.group().lower()


    def set_work_filename(self):
        work_path = self.get_path()
        if os.path.exists(work_path):
            if self.get_select()==0:
                project_name = self.serach_project_name(work_path)
                shot = self.serach_shot_name(work_path)
                department = self.serach_department_name(work_path)
                version = 'v001.01'
                base_name = '_'.join([project_name, shot, department, version])
                base_name = base_name +'.hip'
                abs_path = os.path.join(work_path, base_name)
                return abs_path
    
    def set_random_filename(self):
        work_path = self.get_path()
        if os.path.exists(work_path):
            if self.get_select()==0:
                project_name = os.path.split(work_path)[1]
                aritist = getpass.getuser()
                version = 'v001.01'
                base_name = '_'.join([project_name, aritist, version])
                base_name = base_name + '.hip'
                abs_path = os.path.join(work_path, base_name)
                return abs_path
    def is_work_path(self, work_path):
        project_name = self.serach_project_name(work_path)
        shot = self.serach_shot_name(work_path)
        department = self.serach_department_name(work_path)
        if project_name and shot and department:
            return True
        else:
            return False

            
    def save_file(self, path):
        if self.is_work_path(path):
            abs_path = self.set_work_filename(path)
        else:
            abs_path = self.set_random_filename(path)
        hou.hipFile.setName(abs_path)
        hou.hipFile.save()

    


#todo
#if this hipFile exists Find the lastversion and up the version to save
def main():
    import_path = set_path()
    sence = Sence()
    sence.save_file(import_path)
    
    

if __name__ == '__main__':
    main()