from distutils.filelist import findall
import os
import hou
import re
import getpass


def set_path():
    sel_path = hou.ui.readInput('Set sence',buttons=('Set', 'close'),default_choice=0, close_choice=1, title='Set Sence', initial_contents='copy your work path!')
    return sel_path

#'H:\projects\Football_PV\Production\Sq\S01\VFX\work'
class SaveHip():

    def __init__(self, path) -> None:
        self.path = path
        self.filename = ''

    #获取路径
    def get_path(self):
        return self.set_path()[1]
    
    #获取用户是否确定
    def get_select(self):
        return self.set_path()[0]

    #获取项目名称
    def serach_project_name(self, path):
        pattern = re.compile(r'(?<=projects\\)\w+', re.I)
        finded = pattern.findall(path)
        return finded[0]

    #获取镜头号 
    def serach_shot_name(self, path):
        pattern = re.compile(r's\w+\d+/', re.I)
        finded = pattern.findall(path)
        return finded[0]
    
    #获取组别
    def serach_department_name(self, path):
        pattern = re.compile(r'{cfx | vfx}', re.I)
        matched = pattern.match(path)
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