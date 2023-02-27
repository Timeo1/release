import maya.cmds as cmds

if not cmds.about(batch=True):
    cmds.commandPort(name=":20180", sourceType="mel")
    cmds.commandPort(name=":20181", sourceType="python")
