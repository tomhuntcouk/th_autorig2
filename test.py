import pymel.all as pm

# import globalvars
# from controls import Control
from chain_basic import Jointchain
from skeleton import RigJoint
# from rig_basic import BaseBindrig
# from rig_ikfk import *

"""
p = '/Users/Tom/Developement'

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

	l = 'file -f -options "v=0;"  -esn false  -ignoreVersion  -typ "mayaAscii" -o "/Users/Tom/Developement/th_autorig/assets/autorig_test.ma";addRecentFile("/Users/Tom/Dropbox/SCRIPTS/python/th_autorig/assets/autorig_test.ma", "mayaAscii");'
	pm.mel.eval( l )

	print pm.api.MFnDependencyNode

	# r = RigJoint( name="yay" )
	# print type(RigJoint( 'pelvis_j' ))

	l_arm = Jointchain.from_startend( 
		'left_arm',
		pm.PyNode( 'leftUpperArm_1_j' ), 
		pm.PyNode( 'leftWrist_j' )
	)

	# print l_arm.children(), l_arm.parent()

	# return

	# if( not pm.objExists( 'GEOMETRY_GRP' ) ) :
	# 	globalvars.geometrygrp = pm.group( name='GEOMETRY_GRP', world=True, em=True )
	# if( not pm.objExists( 'SKELETON_GRP' ) ) :
	# 	globalvars.skeletonsgrp = pm.group( name='SKELETON_GRP', world=True, em=True )
	# if( not pm.objExists( 'RIG_GRP' ) ) :
	# 	globalvars.riggrp = pm.group( name='RIG_GRP', world=True, em=True )
	# if( not pm.objExists( '`CONTROLS_GRP' ) ) :
	# 	globalvars.controlsgrp = pm.group( name='CONTROLS_GRP', world=True, em=True )

	# globalvars.ikfkcontrol = Control.ikfkswitcher( pm.PyNode( 'world' ) )

	# l_arm_name = 'left_arm'
	# l_arm = Jointchain.from_startend(
	# 	l_arm_name, 
		# pm.PyNode( 'leftUpperArm_1_j' ), 
		# pm.PyNode( 'leftWrist_j' )
	# )

	# l_arm.orient_chain()

	# l_arm_fkrig = FkChainrig( l_arm_name, l_arm )
	# l_arm_fkrig.create()

	# l_arm_fkrig.tidy()

	# print l_arm.partname, l_arm.subpartname

	# l_arm.duplicate_chain( 'left_arm_duplicate' )

	# return

	

	# # return

	# l_armrig  = BaseBindrig( 'left_arm', l_arm, ( 0, 1 ) )
	# l_armrig.add_rig( 
	# 	'ikfkblend',
	# 	IkFkBlendrig( 'leftArm', l_armrig.bindjointchain )
	# )
	# l_armrig.tidy()

	# l_armrig.connect_bindjoints()


	# l_armrig.tidy()


