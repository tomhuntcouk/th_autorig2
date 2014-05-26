import pymel.all as pm
import pprint

from chain_basic import Jointchain
from rig_basic import *
from rig_ikfk import *
from rig_spline import *
from addin_limbs import *
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

NOTES:

spline ik - bind spline to joints rather than clusters
			copy start and end joints from chain to maintain orient etc



##############################################
"""



def main() :

	pp = pprint.PrettyPrinter( indent=4 )

	# vclass.testJoint()
	# return

	l = 'file -f -options "v=0;"  -esn 	false  -ignoreVersion  -typ "mayaAscii" -o "/Users/Tom/Development/th_autorig2/assets/autorig_test.ma";addRecentFile("/Users/Tom/Development/th_autorig2/assets/autorig_test.ma", "mayaAscii");'
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


	

	# l_arm.orient_jointchain()
	# l_arm.split_rigjoint( 0, 2 )	
	# l_arm.duplicate_jointchain(  )
	# l_arm_rig = BasicRig( l_arm )
	# print l_arm.tree_parent()

	

	chain, torun, twist, stretch, shouldtidy = [None] * 5

	chain = 'arm'
	# chain = 'spine'
	torun = 'ik'
	# torun = 'fk'
	# torun = 'spline'
	# torun = 'blend'
	twist = False
	stretch = True
	shouldtidy = False
	# shouldtidy = True

	if( chain == 'arm' ) :
		l_arm = Jointchain.from_startend( 
			pm.PyNode( 'leftUpperArm_1_j' ), 
			pm.PyNode( 'leftWrist_j' )
		)

		l_arm_rig = BindRig( 
			'leftArm'		
		)
		l_arm_rig.create( 
			l_arm,
			( 1, 2 )
		)

	elif( chain == 'spine' ) :
		spine = Jointchain.from_startend(
			pm.PyNode( 'spine_1_j' ), 
			pm.PyNode( 'neck_1_j' )
			# pm.PyNode( 'leftUpperArm_1_j' ), 
			# pm.PyNode( 'leftWrist_j' )
		)

		spine_rig = BindRig(
			'spine'
		)
		spine_rig.create(
			spine,
			# ( 1, 1 )
		)


	if( torun == 'fk' ) :

		fk_rig = FkRig()
		l_arm_rig.add_child( fk_rig )
		fk_rig.create()
		if twist :
			fk_rig_twist = DistributedTwistAddin()
			fk_rig.add_child( fk_rig_twist )
			fk_rig_twist.create()
		if stretch :
			fk_rig.addinSquashStretch()

		fkw = pm.PyNode('leftWrist_FKJ')
		palm = pm.PyNode('leftPalm_j')
		palm.setParent(fkw)

		if shouldtidy : fk_rig.tidy()

	elif( torun == 'ik' ) :

		ik_rig = IkRig()
		l_arm_rig.add_child( ik_rig )
		ik_rig.create()
		if twist :
			ik_rig_twist = DistributedTwistAddin()
			ik_rig.add_child( ik_rig_twist )
			ik_rig_twist.create()
		if stretch :
			ik_rig.addinSquashStretch()
		
		ikw = pm.PyNode('leftWrist_IKJ')
		palm = pm.PyNode('leftPalm_j')
		# palm.setParent(ikw)

		if shouldtidy : ik_rig.tidy()

	elif( torun == 'blend' ) :

		blendrig = BlendRig()
		l_arm_rig.add_child( blendrig )
		blendrig.create()
		blendrig.add_child( fk_rig )
		blendrig.add_child( ik_rig )
		blendrig.connect_rigs()

		if shouldtidy : l_arm_rig.tidy()

	elif( torun == 'spline' ) :

		splineikfkrig = SplineIkFkRig()
		spine_rig.add_child( splineikfkrig )
		splineikfkrig.create()

		if shouldtidy : spine_rig.tidy()

