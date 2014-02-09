import pymel.all as pm
import pprint

from chain_basic import Jointchain
from rig_basic import *
from rig_ikfk import *
from skeleton import RigJoint

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

	l = 'file -f -options "v=0;"  -esn 	false  -ignoreVersion  -typ "mayaAscii" -o "/Users/Tom/Development/th_autorig/assets/autorig_test.ma";addRecentFile("/Users/Tom/Dropbox/SCRIPTS/python/th_autorig/assets/autorig_test.ma", "mayaAscii");'
	pm.mel.eval( l )
	# print pm.api.MFnDependencyNode
	# RigJoint( name='test' )	
	# print type(pm.PyNode( 'pelvis_j' ))
	# print MyVirtualNode(n='wow')

	for group in settings.staticgroupsdict.items() :
		print group

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
		'left_arm'		
	)
	l_arm_rig.create( 
		l_arm,
		( 1, 2 )
	)

	fk_rig = FkRig()	
	l_arm_rig.add_child( fk_rig )
	# print fk_rig.tree_parent()
	fk_rig.create()
	fk_rig.tidy()



