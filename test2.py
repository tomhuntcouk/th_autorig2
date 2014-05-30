import pymel.all as pm

from rig_basic2 import BindRig, BasicRig
from chain_basic2 import Jointchain
from skeleton2 import RigJoint

# probably put this in __init_.py
pm.factories.registerVirtualClass( BindRig, nameRequired=False )
pm.factories.registerVirtualClass( BasicRig, nameRequired=False )
pm.factories.registerVirtualClass( Jointchain, nameRequired=False )
pm.factories.registerVirtualClass( RigJoint, nameRequired=False )

def main() :

	l = 'file -f -options "v=0;"  -esn 	false  -ignoreVersion  -typ "mayaAscii" -o "/Users/Tom/Development/th_autorig2/assets/autorig_test.ma";addRecentFile("/Users/Tom/Development/th_autorig2/assets/autorig_test.ma", "mayaAscii");'
	pm.mel.eval( l )


	br = BindRig( name='left_arm_rig' )
	jc = Jointchain( 
		name='left_arm_chain',
		startJoint=pm.PyNode( 'leftUpperArm_1_j' ),
		endJoint=pm.PyNode( 'leftWrist_j' ),
		masterJointChain=True
	)

	br.add_child( jc )
	br.create( ( 3, 3 ) )

	basic = BasicRig()
	br.add_child( basic )
	basic.create()