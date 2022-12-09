import hou
import time




def create_node_on_plane(node: str):
    plane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    currentNode = plane.currentNode()
    pos = plane.selectPosition()
    
    try:
        objMergeNode = currentNode.createNode(node)
    except:
        parent = currentNode.parent()
        objMergeNode = parent.createNode(node)
    objMergeNode.setPosition(pos)

    return objMergeNode


def get_clipboard():
    recent_content = hou.ui.getTextFromClipboard()
    while True:
        content = hou.ui.getTextFromClipboard()
        if content != recent_content:
            recent_content = content
    
        return recent_content
    time.sleep(2)


def set_objmerge_parm(node):
    content = get_clipboard()
    node.setParms({'xformtype': 'local', 'objpath1':content})

def main():
    node = create_node_on_plane('object_merge')
    set_objmerge_parm(node)

if __name__ == "__main__":
    main()
