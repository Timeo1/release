import hou
import os
import sys

from PySide2 import QtWidgets, QtUiTools

class ProjectManager(QtWidgets.QWidget):

    def __init__(self):
        super(ProjectManager, self).__init__()

        self.proj = hou.getenv('JOB').replace('\\', '/') + '/'

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(r'X:\studio_config\houdini16.0\houdini\scripts\python\projman\projman.ui')

        self.setproj_btn = self.ui.findChild(QtWidgets.QPushButton, 'setproj')
        self.projname_lbl = self.ui.findChild(QtWidgets.QLabel, 'projname')
        self.projpath_lbl = self.ui.findChild(QtWidgets.QLabel, 'projpath')
        self.scenelist_list = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')

        # create widgets
        # self.btn = QtWidgets.QPushButton('Click Me')
        # self.lblTitle = QtWidgets.QLabel('PROJECT MANAGER')
        # self.label = QtWidgets.QLabel(self.proj)
        # self.listwidget = QtWidgets.QListWidget()

        # create connections
        self.setproj_btn.clicked.connect(self.setproject)

        # self.createInterface()

        # layout
        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.ui)

        # Add widgets to layout
        # mainLayout.addWidget(self.lblTitle)
        # mainLayout.addWidget(self.label)
        # mainLayout.addWidget(self.listwidget)
        # mainLayout.addWidget(self.btn)

        self.setLayout(mainLayout)

    def setproject(self):
        setjob = hou.ui.selectFile(title = 'Set Project', file_type=hou.fileType.Directory)
        hou.hscript('setenv JOB=' + setjob)
        self.proj = hou.getenv('JOB').replace('\\', '/') + '/'

        projname = setjob.split('/')[-2]
        setjob = os.path.dirname(setjob)
        projpath = os.path.split(setjob)[0]

        self.projname_lbl.setText(projname)
        self.projpath_lbl.setText(projpath)

        self.createInterface()

    def openScene(self, item):
        hipFile = self.proj + item.data()
        # open hip file
        hou.hipFile.load(hipFile)


    def createInterface(self):
        self.scenelist_list.clear()

        for file in os.listdir(self.proj):
            if file.endswith('.hip'):
                self.scenelist_list.addItem(file)

        # connect list items to function
        self.scenelist_list.doubleClicked.connect(self.openScene)
