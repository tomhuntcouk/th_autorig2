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

		# get start and end joints
		rigjoints = self.tree_children( 'jointchain' )[0].rigjoints
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

		pm.select( None )

		# create ik spline between them
		ikhandlename = utils.name_from_tags( startjoint, 'ikhandle' )
		pm.ikHandle( 
			startjoint, 
			endjoint,
			solver='ikSplineSolver',
			endEffector=endjoint,
			name=ikhandlename
		)

		# ikeffector.rename( utils.name_from_tags( endjoint, 'ikeffector' ) )
		# self.add_child( ikhandle )