import pymel.all as pm

from tree import TreeNode
# from chain_basic import Jointchain

from rig_basic import *
from rig_ikfk import FkRig
from controls import *
import controls
import utils, settings


class SplineIkRig( BasicRig ) :
	PARTNAME = 'splineRig'

	def create( self, _jointchain=None ) :		
		super( SplineIkRig, self ).create( _jointchain )
		
		jointchain = self.tree_children( 'jointchain' )[0]

		# get start and end joints
		rigjoints = jointchain.rigjoints		
		
		# # create controls and store start/end controls/rigjoints
		controlsdriverslist = []
		for i, rigjoint in enumerate( [ rigjoints[0], rigjoints[-1] ] ) :		

			# create control
			control = RigControl( n=rigjoint.name() )
			control.setRotationOrder(
				utils.aim_axis_to_rotate_order( settings.rotationorder ),
				False
			)
			control.position_to_object( rigjoint )
			self.add_child( control )

			# create driver joint and store it with it's corresponding control
			driverrigjoint = rigjoint.duplicate(
				n=utils.name_from_tags( rigjoint, 'spline', 'driver' )
			)[0]
			self.add_child( driverrigjoint )
			controlsdriverslist.append( ( control, driverrigjoint ) )

		startjoint = jointchain.rigjoints[0]
		startdriver = controlsdriverslist[0][1]
		endjoint = jointchain.rigjoints[-1]
		enddriver = controlsdriverslist[-1][1]

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
		tobind = [ ikcurve ] + [ i[1] for i in controlsdriverslist ]
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
		for control, driver in controlsdriverslist :
			pm.parentConstraint(
				[ control, driver ],
				mo=False
			)


class SplineIkFkRig( BaseRig ) :
	PARTNAME = 'splineRig'

	def __init__( self ) :
		super( SplineIkFkRig, self ).__init__()
		self.splineikrig = SplineIkRig()
		self.add_child( self.splineikrig )
	 	self.fkrig = FkRig()
	 	self.add_child( self.fkrig )

	def create( self, _jointchain=None ) :
		# print self.tree_root()
		self.splineikrig.create( _jointchain )
		self.fkrig.create( _jointchain )

		# now we'll connect the two rigs
		# first hide the start and end controls of teh fkrig
		self.fkrig.tree_children( 'rigControl' )[0].zero_group().hide()
		self.fkrig.tree_children( 'rigControl' )[-1].zero_group().hide()

		# now we can parent the upper spline control to the last fk rigjoint
		pm.parentConstraint(
			[ self.fkrig.tree_children( 'jointchain' )[0].rigjoints[-1],
			self.splineikrig.tree_children( 'rigControl' )[-1].zero_group() ],
			mo=True
		)

