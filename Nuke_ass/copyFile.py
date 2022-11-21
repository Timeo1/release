import os
import re
import shutil
import sys
import nuke
import nukescripts


class CopyFile(object):

    def __init__(self):
        self.input_nodes = []
        self.new_path = []
        
    def sele_node(self):
        node = nuke.selectedNode()
        return node

    def find_connect_nodes(self, node):
        if node.Class() == "Read" and node:
            if node not in self.input_nodes:
                self.input_nodes.append(node)
        else:
            if node:
                min_nodes = node.minInputs()
                for i in range(min_nodes):
                    _node = node.input(i)
                    if _node:
                        self.find_connect_nodes(_node)
                    else:
                        continue
        return self.input_nodes

    def get_reads_path(self, input_nodes, method):
        finalmsg = []
        for i in input_nodes:
            name = nuke.filename(i)
            if name is None:
                continue
            if method == "file":
                curname = os.path.basename(name)
            if method == "dir" or method == "":
                curname = os.path.dirname(name)
            if method == "long":
                curname = name

            curname = re.sub("\.%.*", "", curname)
            finalmsg.append(curname) 
        return finalmsg


    def target_path(self, path):
        version = ""
        ver = re.compile(r"v\d+")
        pattern = re.compile(r".*vfx/", re.I)
        _a = pattern.match(path)
        _v = ver.findall(path)
        source_path = _a.group()
        version = _v[0]
        target_path=  source_path + "torender/" + version
        return target_path


    def get_connect_nodes(self):
        node = self.sele_node()
        nodes = self.find_connect_nodes(node)
        return nodes

    def get_target_paths(self):
        nodes = self.get_connect_nodes()
        paths = self.get_reads_path(nodes, 'long')
        target_path = self.target_path(paths[0])
        return target_path
    
    def copy_files(self):
        nodes = self.get_connect_nodes()
        paths = self.get_reads_path(nodes, 'dir') 
        names= self.get_reads_path(nodes, 'file') 
        z = zip(paths, names, nodes)
        for dir, name, node in z:
            target = self.get_target_paths()
            dirname = os.path.split(dir)[1]
            target_name = target + "/" + dirname +"/"
            
            if not os.path.exists(target_name):
                target_dir = os.makedirs(target_name)  
            filetype = re.compile(r".*.exr$")
            isexr = filetype.match(name)
            if isexr:
                seq_name = name
            else:
                seq_name = name + ".%04d.exr"
            input_file = os.path.join(target_name, seq_name)
            node['file'].setValue(input_file)
 
            for file in os.listdir(dir):
                if isexr:
                    basename = re.sub("####", r"\d+",name)
                else:
                    basename = name+"."+"\d+"+".exr"

                pattern = re.compile(basename)
                matched = pattern.match(file)
                if matched:
                    file_fullpath = os.path.join(dir, file)
                    try:
                        shutil.copy2(file_fullpath, target_name)
                    except IOError as e:
                        print("Unable to copy file.%s" % e) 
                    except:
                        print("Unexpected error:", sys.exc_info())
    
    def save_as_newone(self):
        filename = nuke.root()['name'].value()
        filename = os.path.split(filename)[1]
        target_path = self.get_target_paths()
        new_filename = os.path.join(target_path, filename)
        nuke.scriptSaveAs(filename=new_filename, overwrite=-1)
    

    
    
def main():
    CopyFile().copy_files()
    CopyFile().save_as_newone()


    
