import nuke
import copyFile

#nuke.addOnscriptLoad(copyFile)



nuke.menu("Nuke").addMenu("vfx").addCommand("CopyFile", "copyFile.main()", shortcut="")