#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'LiDong'

import os
if os.environ.get('DEV'):
    from init_hrpyc import hou, ui
else:
    import hou
import toolutils
import soptoolutils


def main():
    v = toolutils.sceneViewer()
    sel = hou.selectedNodes()
    if sel:
        paint = toolutils.findChildNodeOfTypeWithParms(sel[0],
                                                      'paint',
                                                      {'overridecd': 1, 'cdname': 'density'})
        if paint:
            paint.setCurrent(True)
            v.enterCurrentNodeState()
            return

    scatter_geo = v.selectObjects('Please select object to copy to',
                                  use_existing_selection=False,
                                  allowed_types=('geo',),
                                  allow_multisel=False)

    source_geo = v.selectObjects('Please select source',
                                  use_existing_selection=False,
                                  allowed_types=('geo',))
    # 如果啥都没选。不报错。
    if not (scatter_geo and source_geo):
        return
    elif len(scatter_geo) > 1 or len(source_geo) > 1:
        hou.ui.displayMessage('Please select one geometry object')
        return
    scatter_geo, = scatter_geo
    source_geo, = source_geo

    geo = hou.node('/obj').createNode('geo', 'copy', run_init_scripts=False)
    merge_source = geo.createNode('object_merge', 'merge_source')
    merge_source.parm('objpath1').set(source_geo.path())
    merge_source.parm('xformtype').set(1)

    merge_scatter = geo.createNode('object_merge', 'merge_scatter')
    merge_scatter.parm('objpath1').set(scatter_geo.path())
    merge_scatter.parm('xformtype').set(1)

    scatter_geo.setDisplayFlag(False)
    source_geo.setDisplayFlag(False)

    paint = soptoolutils.buildPaintNode(merge_scatter, None,
                                        parms={'overridecd': 1, 'cdname': "density"},
                                        props={'attribdef': 0, 'fqcolor': 0.4, 'opacity': 0.3, 'radius': 1})

    scatter_sop = geo.createNode('scatter')
    scatter_sop.parm('usedensityattrib').set(1)
    scatter_sop.parm('forcetotal').set(0)
    scatter_sop.parm('emergencylimit').set(500)
    scatter_sop.setInput(0, paint)

    copy_sop = geo.createNode('copy')
    copy_sop.parm('pack').set(True)
    copy_sop.setInput(0, merge_source)
    copy_sop.setInput(1, scatter_sop)
    copy_sop.setDisplayFlag(True)
    copy_sop.setRenderFlag(True)

    geo.layoutChildren()
    paint.setCurrent(True)
    v.enterCurrentNodeState()
if __name__ == '__main__':
    main()