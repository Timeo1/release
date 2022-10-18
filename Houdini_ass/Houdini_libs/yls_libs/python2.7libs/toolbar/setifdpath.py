# -*- coding: utf-8 -*-

import re
import hou

nodes = hou.selectedNodes()
def main():
	for node in nodes:
		basename = hou.hipFile.basename().split('_')
		if len(basename) > 2:
			version = basename[-2]
			mc = re.match(r'v\w+', version)
			if mc is not None:
				parm = node.parm('vm_picture')
				fullpath = "$HIP/render_out/%s/`opname('.')`/`opname('.')`_%s.$F4.exr" % (version, version)
				parm.set(fullpath)