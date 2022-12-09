from requests import delete
import hou
import re


class CreatMantra(object):
    def __init__(self):
        self.camera_list = []
        self.len = 0

    #获取obj层级下的摄像机
    def findCamera(self):
        obj = hou.node('/obj')
        for node in obj.children():
            if node.type().name() == 'cam':
                self.camera_list.append(node)
        return self.camera_list

    #如果没有相机则创建相机，如果有则优先选择和命名匹配的相机
    def selectRenderCamera(self):
        cam_list = self.findCamera()
        self.len = len(cam_list)

        if self.len == 0:
            return self.createCamera() 
        if self.len >= 1:
            pattern = re.compile('render_?camera[\d]?', re.I)
            for cam in self.camera_list:
                match = pattern.match(cam.name())
                if match:
                    return cam
            else:
                return self.camera_list[0]

    #创建相机
    def createCamera(self):
        cam = hou.node('/obj').createNode('cam', 'Render_Camera')
        return cam
    
    #如果有ropnet节点
    def isHaveRopnet(self):
        obj =  hou.node("/obj")
        nodes = obj.children()
        for node in nodes:
            if node.type().name() == 'ropnet':
                return node
    
    #指定一个特定位置的输出路径
    def setpath(self):
        output_path = r'$HIP/render/v001/$OS/$HIPNAME.$OS.$F4.exr'
        return output_path
    
    #设置mantra参数
    def setMantraParm(self, mantra, geo_name):
        output = self.setpath()
        Cam  = self.selectRenderCamera()
        camera = Cam.path()
        
        mantra.parm('vm_picture').set(output)
        mantra.parm('camera').set(camera)
        mantra.parm('forceobject').set(geo_name)
        mantra.parm('vobject').set('')
        
    #创建Mantra并设置参数
    def createMantra(self, geo_name):
        if self.isHaveRopnet():
            rop = self.isHaveRopnet()
            mantra = rop.createNode('ifd', geo_name)
        else:
            mantra = hou.node('/out').createNode('ifd', geo_name)

        self.setMantraParm(mantra, geo_name)
        return mantra
    


        
        
def main():
    nodes = hou.selectedNodes()
    i = 0
    for n in nodes:
        geo_name = n.name()
        mn = CreatMantra().createMantra(geo_name)
        mn.move((0,i))
        i += 1 

        
if __name__ == '__main__':
    main()
        

        
        
            

    