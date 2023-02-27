import os 
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets


class network(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.init_Value()

    def init_Value(self):
        self.MOUSEPRESSPOS = QtCore.QPoint(0, 0)
        self.STARTLINKPOS = QtCore.QPoint(0, 0)
        self.STARTLINK_STAT = 0
    #-----------------------------------------------# 
    def rightMenuShow(self):
        try:
            self.contextMenu = QtWidgets.QMenu(self)
            self.actionA = self.contextMenu.addAction("createNode")
            self.contextMenu.popup(QtGui.QCursor.pos())
            self.parent().NETWORKMUNU_POS = QtGui.QCursor.pos()
            self.actionA.triggered.connect(self.parent().createNode)
            self.contextMenu.show()
        except:
            pass



    def get_ActiveNode(self):
        pass

    def start_link(self, stat):
        if self.parent().ACTIVENODE != None:
            self.STARTLINK_STAT = 1
            nodex = self.parent().ACTIVENODE.x()
            nodey = self.parent().ACTIVENODE.y()
            if stat == 0:
                innode = self.parent().ACTIVENODE.INNODE
                self.STARTLINKPOS = QtCore.QPoint(innode.x() + nodex,  innode.y() + nodey)
            if stat == 1:
                outnode = self.parent().ACTIVENODE.OUTNODE
                self.STARTLINKPOS = QtCore.QPoint(outnode.x() + nodex, outnode.y() + nodey)
        self.update()
                
    def refreshLinks(self):
        self.update()
        for i in self.parent().ALLNODES:
            pass

   #-----------------------------------------------# 
    def setGeo(self, x, y, w, h):
        self.setGeometry(x,y,w,h)
    
    def mousePressEvent(self, event):
        mousepos = event.pos()
        self.MOUSEPRESSPOS = mousepos
        # print("mousePressEvent")

        
    def mouseMoveEvent(self, event):
        mousepos = self.parent().mapFromGlobal(event.globalPos())
        self.MOVEPOS = mousepos
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(QtCore.QPoint(mousepos.x() -self.MOUSEPRESSPOS.x(), mousepos.y() - self.MOUSEPRESSPOS.y()))
        self.update()
        event.accept()

    def mouseReleaseEvent(self, event):
        # self.ACTIVENODE = None
        self.STARTLINK_STAT = 0
        self.parent().STARTLINKSTAT = 0
        self.update()
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
        for i in range(11):
            qp.drawLine( QtCore.QPoint(0, (float(i)/10.0)*h),
                         QtCore.QPoint(w, (float(i)/10.0)*h)
            )
            qp.drawLine( QtCore.QPoint((float(i)/10.0)*w, 0),
                         QtCore.QPoint((float(i)/10.0)*w, h)
            )
        
        if self.STARTLINK_STAT == 1:
            qp.drawLine(self.STARTLINKPOS, self.MOVEPOS)
        # qp.drawLine( QtCore.QPoint(0, 1), QtCore.QPoint(w,h))

        for i in self.parent().ALLNODES:
            x = i.x()
            y = i.y()
            w = i.width()
            h = i.height()
            inputs = i.getInputs()
            for input in inputs:
                ix = input.x()
                iy = input.y()
                iw = input.width()
                ih = input.height()
                qp.drawLine(
                            QtCore.QPoint(x+w/2, y),
                            QtCore.QPoint(ix+iw/2, iy+ih)
                )
        

