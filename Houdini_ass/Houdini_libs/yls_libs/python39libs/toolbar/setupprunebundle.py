import hou
def SetupPruneBundle(kwargs):
    def add_nodes(bundle, nodes):
        for node in nodes:
            bundle.addNode(node)
            node.setColor(pruneColor)
    
    pruneColor = hou.Color([0.05,0.05,0.05])
    defColor = hou.Color([0.8,0.8,0.8])
    sel = hou.selectedNodes()
    bundle = hou.nodeBundle('prune')
    if bundle:
        if kwargs['altclick'] and not kwargs['ctrlclick']:
            if sel:
                for node in sel:
                    bundle.removeNode(node)
                    node.setColor(defColor)
        elif kwargs['altclick'] and kwargs['ctrlclick']:
            nodes = bundle.nodes()
            bundle.destroy()
            for node in nodes:
                node.setColor(defColor)
            return
        elif sel:
            add_nodes(bundle, sel)
    else:
        bundle = hou.addNodeBundle('prune')
        if sel:
            add_nodes(bundle, sel)

def main(kwargs):
    SetupPruneBundle(kwargs)