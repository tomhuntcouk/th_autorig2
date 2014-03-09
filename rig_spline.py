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
		# rigjoints = jointchain.rigjoints		
		
		# # create controls and store start/end controls/rigjoints
		controlslist = []
		driverslist = []
		for i, rigjoint in enumerate( jointchain.rigjoints ) :
			prevrigjoint = None
			try : prevrigjoint = jointchain.rigjoints[ i - 1 ]
			except : pass

			control = RigControl( n=rigjoint.name() )
			control.setRotationOrder(
				utils.aim_axis_to_rotate_order( settings.rotationorder ),
				False
			)
			control.position_to_object( rigjoint, prevrigjoint )
			self.add_child( control )
			controlslist.append( control )

			driverrigjoint = rigjoint.duplicate(
				n=utils.name_from_tags( rigjoint, 'spline', 'driver' )
			)[0]
			self.add_child( driverrigjoint )
			driverslist.append( driverrigjoint )

		startjoint = jointchain.rigjoints[0]
		startdriver = driverslist[0]
		startcontrol = controlslist[0]
		endjoint = jointchain.rigjoints[-1]
		enddriver = driverslist[-1]
		endcontrol = controlslist[-1]

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
		tobind = [ ikcurve ] + driverslist
		pm.skinCluster( 
			tobind,
			bindMethod=0,
			maximumInfluences=len( tobind ) - 1,
		)

		# set twist control
		ikhandle.dTwistControlEnable.set( True )
		ikhandle.dWorldUpType.set( 4 )
		startdriver.worldMatrix[0] >> ikhandle.dWorldUpMatrix
		enddriver.worldMatrix[0] >> ikhandle.dWorldUpMatrixEnd

		# parent drivers to controls
		for control, driver in zip( controlslist, driverslist ) :
			pm.parentConstraint(
				[ control, driver ],
				mo=False
			)

		# point constraint intermediate controls
		# maintaining distance between start and end controls
		# for control in controlslist[1:-1] :
		# 	# tostartcontrol = utils.distance_between( startcontrol, control )
		# 	# toendcontrol = utils.distance_between( endcontrol, control )
		# 	# print tostartcontrol / toendcontrol
		# 	pm.pointConstraint(
		# 		[ startcontrol, endcontrol, control.zero_group() ],
		# 		mo=True
		# 	)

		# # set up orient constraints for fk
		for i, control in enumerate( controlslist ) :
			if( i > len( controlslist ) - 2 ) : break
			nextcontrolzero = controlslist[ i + 1 ].zero_group()			
			if( nextcontrolzero ) :
				pm.orientConstraint(
					[ control, nextcontrolzero ],
					mo=True
				)




