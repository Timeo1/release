# -*- coding: utf-8 -*-

import re
import hou
import os

# SGS_S100_c020_vfx_sha_v001_dli


def main():
	basename = hou.hipFile.basename()
	filename = os.path.splitext(basename)[0]
	basenamesp = filename.split('_')
	se = basenamesp[1]
	sh = basenamesp[2]
	grp = basenamesp[3]
	des = basenamesp[4]
	ver = basenamesp[5]
	psn = basenamesp[6]
	print se
	print sh
	print grp
	print des
	print ver
	print psn
	nodes = hou.selectedNodes()
	mc = re.match(r'NEG\w+?_\w+?_vfx_\w+?_v\d+?_\w+?', filename)
	basepath = r'X:/NvErGuo_NRG_180203/3D/fxrender'
	if mc is not None:
		cntpath = os.path.join(se, sh, des, ver, "`opname(\'.\')`")
		basefilename = 'NEG_'+ '_'.join([se,sh,grp,des,ver,psn])
		renderpath = os.path.join(basepath,cntpath).replace('\\','/')
		for node in nodes:
			print basefilename
			parm = node.parm('vm_picture')
			fullpath = renderpath + '/' + basefilename + '_`opname(\'.\')`' + '.$F4' + '.exr'
			parm.set(fullpath)