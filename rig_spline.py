import pymel.all as pm

from tree import TreeNode
# from chain_basic import Jointchain

from rig_basic import *
from controls import *
import controls
import utils, settings


class SplineRig( BasicRig ) :
	PARTNAME = 'splineRig'

	def create( self, _jointchain=None ) :
		super( SplineRig, self ).create( _jointchain )
		jointchain = self.tree_children( 'jointchain' )[0]

		# get start and end joints
		rigjoints = jointchain.rigjoints
		startjoint = rigjoints[0]
		endjoint = rigjoints[-1]
		
		# create controls at start and end
		startcontrol = RigControl( n=startjoint.name() )
		startcontrol.setRotationOrder( 
			utils.aim_axis_to_rotate_order( settings.rotationorder ),
			False
		)
		startcontrol.position_to_object( startjoint )
		self.add_child( startcontrol )

		endcontrol = RigControl( n=endjoint.name() )
		endcontrol.setRotationOrder( 
			utils.aim_axis_to_rotate_order( settings.rotationorder ),
			False
		)
		endcontrol.position_to_object( endjoint )
		self.add_child( endcontrol )

		# create driver joints to bind curve to
		startdriverjoint = startjoint.duplicate( 
			n=utils.name_from_tags( startjoint, 'spline', 'driver' )
		)[0]
		self.add_child( startdriverjoint )

		enddriverjoint = endjoint.duplicate(
			n=utils.name_from_tags( endjoint, 'spline', 'driver' )
		)[0]
		self.add_child( enddriverjoint )

		# create ik spline between them
		ikhandlename = utils.name_from_tags( startjoint, 'ikhandle' )
		ikhandle, ikeffector, ikcurve = pm.ikHandle( 
			startJoint=startjoint, 
			endEffector=endjoint,
			solver='ikSplineSolver',
			numSpans=len( jointchain.rigjoints ) - 1,
			name=ikhandlename
		)
		ikeffector.rename( utils.name_from_tags( endjoint, 'ikeffector' ) )
		ikcurve.rename( utils.name_from_tags( startjoint, 'curve' ) )
		self.add_child( ikhandle )
		self.add_child( ikcurve )

		# bind curve to driver joints
		tobind = [ ikcurve, startdriverjoint, enddriverjoint ]
		pm.skinCluster( 
			tobind,
			bindMethod=0,
			maximumInfluences=len( tobind ) - 1,
		)

		# set twist control
		ikhandle.dTwistControlEnable.set( True )
		ikhandle.dWorldUpType.set( 4 )
		startdriverjoint.worldMatrix[0] >> ikhandle.dWorldUpMatrix
		enddriverjoint.worldMatrix[0] >> ikhandle.dWorldUpMatrixEnd

		# parent driver joints to controls
		pm.parentConstraint(
			[ startcontrol, startdriverjoint ],
			mo=False
		)
		pm.parentConstraint(
			[ endcontrol, enddriverjoint ],
			mo=False
		)








