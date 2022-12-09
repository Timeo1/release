import os
import hou
import re
import getpass


def set_path():
    sel_path = hou.ui.readInput('Set sence',buttons=('Set', 'close'),default_choice=0, close_choice=1, title='Set Sence', initial_contents='copy your work path!')
    return sel_path

#'H:\projects\Football_PV\Production\Sq\S01\VFX\work'
class SaveHip():

    def __init__(self) -> None:
        self.path = ''
        self.filename = ''

    def set_path(self):
        sel_path = hou.ui.readInput('Set sence',buttons=('Set', 'close'),default_choice=0, close_choice=1, title='Set Sence', initial_contents='copy your work path!')
        self.path = sel_path
        return self.path

    #获取路径
    def get_path(self):
        return self.path[1]
    
    #获取用户是否确定
    def get_select(self):
        return self.path[0]

    #获取项目名称
    def serach_project_name(self, path):
        pattern = re.compile(r'(?<=projects\\)\w+', re.I)
        finded = pattern.findall(path)
        if finded:
            return finded[0]
        else:
            return False

    #获取镜头号 
    def serach_shot_name(self, path):
        pattern = re.compile(r's\w*\d+', re.I)
        finded = pattern.findall(path)
        if finded:
            return finded[0]
        else:
            return False
    
    #获取组别
    def serach_department_name(self, path):
        pattern = re.compile(r'[c|v|e]fx', re.I)
        finded = pattern.findall(path)
        if finded:
            return finded[0].lower()
        else:
            return False
    
    #查找是否是最后一个版本
    def is_last_version(path, filename):
        hiplist = os.listdir(path)
        count1 = hiplist.count(filename)
        if count1 > 0 :
            return True
        else:
            return False

    #检查是否是新文件
    def isNewFile1(self):
        return hou.hipFile.isNewFile()


    #设置工作文件名
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
    
    #如果不是工作路径  随便设置一个文件名
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

    #判断是否是工作路径
    def is_work_path(self, work_path):
        project_name = self.serach_project_name(work_path)
        shot = self.serach_shot_name(work_path)
        department = self.serach_department_name(work_path)
        if project_name and shot and department:
            return True
        else:
            return False
    
    def update_version(self):
        basename = hou.hipFile.basename()
        pattern = re.compile(r"v\d+.*\d", re.I)
        hfn = hou.hipFile.name()
        hfd =  os.path.dirname(hfn)
        try:
            version = pattern.findall(basename)[0]
        except IndexError:
            version = None
            print("Has no version attribute!")

        if version:
            version_up =  version[:-2] + str(int(version[-2:])+1).zfill(2)
            basename = pattern.sub(version_up, basename)
            basename = hfd + os.sep + basename

        else:
            version_up = 'v001.01'
            namelist = basename.split(".")
            namelist.insert(-1, version_up)
            basename = '_'.join(namelist[:-1])
            basename += '.hip'
            basename = hfd + os.sep + basename
            
        return basename
        

    #保存文件        
    def save_file(self):
        if self.isNewFile1():
            self.set_path()
            path = self.get_path()
            if self.is_work_path(path):
                abs_path = self.set_work_filename()
            else:
                abs_path = self.set_random_filename()
            if abs_path:
                hou.hipFile.setName(abs_path)
                hou.hipFile.save()
                hou.ui.displayMessage("Success save to NewHip!")
            
        else:
            abs_path = self.update_version()
            hou.hipFile.setName(abs_path)
            hou.hipFile.save()
            hou.ui.displayMessage("Success up to Version!")



#todo
#if this hipFile exists Find the lastversion and up the version to save
def main():
    hip= SaveHip()
    hip.save_file()
    
    

if __name__ == '__main__':
    main()