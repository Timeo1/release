import maya.cmds as cmd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def utf_8String(StringT):
    utf_8String = StringT
    utf_8String.encode('utf-8')
    utf_8String = unicode(utf_8String, "utf-8")
    return utf_8String
def checkSelect():
    list_select = []
    if cmd.ls(sl = True) != []:
        list_select = cmd.ls(sl=True)
        return list_select
    else:
        return []

def centerPivot():
    for i in checkSelect():
        cmd.xform(i, centerPivots=True)

def pivotMoveToWorldPositon000():
    for i in checkSelect():
        Name = i
        cmd.move(0, 0, 0, Name+'.rotatePivot', Name+'.scalePivot', rpr=True)
        cmd.makeIdentity(Name, a=True)



def meshMoveToWorldPosition000AndClean():
    centerPivot()
    for i in checkSelect():
        cmd.move(0, 0, 0, i,rpr=True)
        cmd.makeIdentity(i, a=True)

def exportMesh():
    #selObj = cmds.ls(sl = 1)
    path = '/*存储路径*/'
    #FileName = selObj
    for i in checkSelect():
        mainPath = path +'/' +i
        cmd.file(mainPath, pr=1, es=1, force=1, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1",type="FBX export")


def mainGui():
    windowName = 'Export_Tool'
    windowTitle = 'Export_Tool1.0'

    try:
        cmd.deleteUI(windowName)
    except:
        pass
    cmd.window(windowName,title = windowTitle)
    cmd.columnLayout(adj = True)

    explain_ZeroPivot = utf_8String('')
    explain_Clean = utf_8String('')
    explain_Export = utf_8String('')

    cmd.button(l='ZeroPivot',ann = explain_ZeroPivot, h=60, w=20, c='pivotMoveToWorldPositon000()')
    cmd.button(l='ZeroMeshClean', ann=explain_Clean, h=60, w=20, c='meshMoveToWorldPosition000AndClean()')
    cmd.button(l='Export', ann=explain_Export, h=60, w=20, c='exportMesh()')

    cmd.showWindow(windowName)


mainGui()