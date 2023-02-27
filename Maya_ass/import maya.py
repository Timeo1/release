import sys
import maya.api.OpenMaya as api

def maya_userNewAPI():
    pass
api.MP
class HelloWorldCmd(api.MPxCommand):
    kCmdName = 'helloWorld'

    def __init__(self) -> None:
        super().__init__(self)

    @staticmethod
    def creator():
        return HelloWorldCmd()
    
    def doIt(self, arg_list):
        print('Hello World')

def initializePlugin(mobject):
    fn_plugin = api.MFnPlugin(mobject)
    try:
        fn_plugin.registerCommand(
            HelloWorldCmd.kCmdName,
            HelloWorldCmd.creator
        )
    except:
        sys.stderr.write('Failed to register command:' + HelloWorldCmd.kCmdName)

def uninitializePlugin(mobject):
    fn_plugin = api.MFnPlugin(mobject)
    try:
        fn_plugin.deregisterCommand(
            HelloWorldCmd.kCmdName,
        )
    except:
        sys.stderr.write('Failed to deregister command:' + HelloWorldCmd.kCmdName)

