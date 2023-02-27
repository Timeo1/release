import os
import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
#-------------------------------------------#
# import sys
# sys.path.append("D:\\release\\Houdini_ass\\Houdini_libs\\yls_libs\\python39\\nodetree")
import nodetree.my_network as network
import nodetree.my_node as node

import importlib
importlib.reload(network)
importlib.reload(node)


class nodetree(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.init_Value()
        self.init_UI()

    
    def init_Value(self):
        self.ALLNODES = []                    #记录所有节点
        self.ACTIVENODE = None                #记录单个激活的节点
        self.ACTIVENODES = []                 #记录激活的所有节点
        self.STARTLINKSTAT = 0          #记录开始连接的节点的状态
        self.LINKIO = 0
        self.NODEW = 200
        self.NODEH = 100
        self.NETWORKMUNU_POS = QtCore.QPoint(0, 0)
    
    def set_ActiveNode(self, node):
        self.ACTIVENODE = node
        self.ACTIVENODES = []
        

    def start_link(self, stat):
        if self.ACTIVENODE != None:
            self.LINKIO = stat
            self.STARTLINKSTAT = 1
            self.mainUI.start_link(stat)
    def refreshLinks(self):
        for i in self.ALLNODES:
            pass
        self.mainUI.refreshLinks()

    def createNode(self):
        self.node = node.node(self.mainUI)
        node_pos = self.mapFromGlobal(self.NETWORKMUNU_POS)
        self.node.setGeo(node_pos.x(), node_pos.y(), self.NODEW, self.NODEH)
        self.node.show()
        self.ALLNODES.append(self.node)


    def init_config(self):
        pass

    def init_UI(self):
        self.mainUI = network.network(self)


    def setGeo(self, x, y, w, h):
        self.setGeometry(x,y,w,h)
        self.mainUI.setGeo(0, 0, w, h)
    
    

    
def onCreateInertface():
    global NOTETREE_APP
    NOTETREE_APP = nodetree()
    NOTETREE_APP.setGeo(300, 300, 1200, 800)
    NOTETREE_APP.show()
    return NOTETREE_APP
onCreateInertface()