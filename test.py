import pymel.all as pm
import pprint

from chain_basic import Jointchain
from rig_basic import *
from rig_ikfk import *
from skeleton import RigJoint
from controls import RigControl

import settings

"""
p = '/Users/Tom/Development'

import sys
import pymel.core as pm
if p not in sys.path :
    sys.path.append( p )
    
    
import th_autorig
reload( th_autorig )

th_autorig.test.main()

"""

"""
##############################################



##############################################
"""



def main() :

	pp = pprint.PrettyPrinter( indent=4 )

	# vclass.testJoint()
	# return

	l = 'file -f -options "v=0;"  -esn 	false  -ignoreVersion  -typ "mayaAscii" -o "/Users/Tom/Development/th_autorig/assets/autorig_test.ma";addRecentFile("/Users/Tom/Development/th_autorig/assets/autorig_test.ma", "mayaAscii");'
	pm.mel.eval( l )
	# print pm.api.MFnDependencyNode
	# RigJoint( name='test' )	
	# print type(pm.PyNode( 'pelvis_j' ))
	# print MyVirtualNode(n='wow')

	for group in settings.staticgroupsdict.values() :
		pm.group( n=group, empty=True, world=True )

	staticcontrolgroup = utils.make_groups_from_path_list( 
		[ 'static' ],
		pm.PyNode( settings.staticgroupsdict[ 'controls' ] )
	)[0]

	for control in settings.staticcontrols.values() :
		c = RigControl( n=control )
		c.zero_group().setParent( staticcontrolgroup )

	l_arm = Jointchain.from_startend( 
		# 'left_arm',
		pm.PyNode( 'leftUpperArm_1_j' ), 
		pm.PyNode( 'leftWrist_j' )
	)

	# l_arm.orient_jointchain()
	# l_arm.split_rigjoint( 0, 2 )	
	# l_arm.duplicate_jointchain(  )
	# l_arm_rig = BasicRig( l_arm )
	# print l_arm.tree_parent()

	l_arm_rig = BindRig( 
		'leftArm'		
	)
	l_arm_rig.create( 
		l_arm,
		( 1, 2 )
	)

	fk_rig = FkRig()
	l_arm_rig.add_child( fk_rig )
	fk_rig.create()
	# fk_rig.tidy()


	ik_rig = IkRig()
	l_arm_rig.add_child( ik_rig )
	ik_rig.create()	
	# ik_rig.tidy()

	blendrig = BlendRig()
	l_arm_rig.add_child( blendrig )
	blendrig.create()
	blendrig.add_child( fk_rig )
	blendrig.add_child( ik_rig )
	blendrig.connect_rigs()

	l_arm_rig.tidy()




