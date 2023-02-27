import os
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets


class indot(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.init_Value()
    
    
    def init_Value(self):
        self.MOUSEPRESSPOS = QtCore.QPoint(0, 0)

    def setGeo(self, x, y, w, h):
        self.setGeometry(x,y,w,h)

    def mousePressEvent(self, event):
        self.parent().DOTFOUCES = 1  
        if self.parent().parent().parent().ACTIVENODE == self.parent():
            self.parent().start_link(0)
        if self.parent().parent().parent().ACTIVENODE != None:
            if self.parent().parent().parent().ACTIVENODE != self.parent():
                if self.parent().parent().parent().STARTLINKSTAT == 1:
                    if self.parent().parent().parent().LINKIO == 1:
                        self.parent().addInput(self.parent().parent().parent().ACTIVENODE)
                        self.parent().parent().parent().refreshLinks()
        # event.accept()

    def mouseReleaseEvent(self, event):
        self.parent().DOTFOUCES = 0
        event.accept()

    # -------------- UI refresh proc --------------#
    # 1 paintEvent
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()
    
    # 2 drawRectangles
    def drawRectangles(self, qp):
        w = self.width()
        h = self.height()
        qp.setBrush(QtGui.QColor(200, 100, 100, 255))
        qp.drawRect(0,0,w,h)

class outdot(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.init_Value()
    
    
    def init_Value(self):
        self.MOUSEPRESSPOS = QtCore.QPoint(0, 0)

    def setGeo(self, x, y, w, h):
        self.setGeometry(x,y,w,h)

    def mousePressEvent(self, event):
        self.parent().DOTFOUCES = 1
        if self.parent().parent().parent().ACTIVENODE == self.parent():
            self.parent().start_link(1)
        if self.parent().parent().parent().ACTIVENODE != None:
            if self.parent().parent().parent().ACTIVENODE != self.parent():
                if self.parent().parent().parent().STARTLINKSTAT == 0:
                    if self.parent().parent().parent().LINKIO == 0:
                        print("aaaa")
        # event.accept()

    def mouseReleaseEvent(self, event):
        self.parent().DOTFOUCES = 0
        event.accept()

    # -------------- UI refresh proc --------------#
    # 1 paintEvent
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()
    
    # 2 drawRectangles
    def drawRectangles(self, qp):
        w = self.width()
        h = self.height()
        qp.setBrush(QtGui.QColor(200, 100, 100, 255))
        qp.drawRect(0,0,w,h)


class node(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.init_Value()
        self.init_UI()
    
    def init_Value(self):
        self.INPUTS = []

        self.MOUSEPRESSPOS = QtCore.QPoint(0, 0)
        self.DOTFOUCES= 0
    # ------------------------------------------------------ #
    def start_link(self, stat):
        self.parent().parent().start_link(stat)
        if stat == 0:
            pass
        if stat == 1:
            pass

    def addInput(self, node):
        if node not in self.INPUTS:
            self.INPUTS.append(node)
    
    def getInputs(self):
        return self.INPUTS

    # ------------------------------------------------------ #
    def init_UI(self):
        self.INNODE = indot(self)
        self.OUTNODE = outdot(self)

    def setGeo(self, x, y, w, h):
        self.setGeometry(x,y,w,h)
        self.INNODE.setGeo(w/2-10, 0, 20, 20)
        self.OUTNODE.setGeo(w/2-10, h-20, 20, 20)
    
    def mousePressEvent(self, event):
        if self.DOTFOUCES == 0:
            mousepos = event.pos()
            self.MOUSEPRESSPOS = mousepos
            self.parent().parent().set_ActiveNode(self)
            print(self)

        
    def mouseMoveEvent(self, event):
        if self.DOTFOUCES == 0:
            mousepos = self.parent().mapFromGlobal(event.globalPos())
            self.MOVEPOS = mousepos
            if event.buttons() & QtCore.Qt.LeftButton:
                self.move(QtCore.QPoint(mousepos.x() -self.MOUSEPRESSPOS.x(), mousepos.y() - self.MOUSEPRESSPOS.y()))
            event.accept()

    def mouseReleaseEvent(self, event):
        # self.ACTIVENODE = None
        event.accept()

    # -------------- UI refresh proc --------------#
    # 1 paintEvent
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()
    
    # 2 drawRectangles
    def drawRectangles(self, qp):
        w = self.width()
        h = self.height()
        qp.setBrush(QtGui.QColor(200, 200, 200, 225))
        qp.drawRect(0,0+20,w,h-40)

