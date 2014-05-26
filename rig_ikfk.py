import pymel.all as pm
import pymel.core.nodetypes as pn

from rig_basic import *
import controls
import utils, settings


class FkRig( BasicRig ) :
	PARTNAME = 'fkRig'

	# def __init__( self ) :
	# 	super( FkRig, self ).__init__()

	def create( self, _jointchain=None ) :
		super( FkRig, self ).create( _jointchain )

		lastcontrol = None
		rigjoints = self.tree_children( 'jointchain' )[0].rigjoints
		if( not len( rigjoints ) ) :
			utils.err( 'FkRig has no jointchains. Cannot create fk rig.' )
			return False


		for rigjoint in rigjoints :
			control = controls.RigControl( n=rigjoint.name() )
			control.setRotationOrder( 
				utils.aim_axis_to_rotate_order( settings.rotationorder ),
				False
			)
			control.position_to_object( rigjoint )
			pm.orientConstraint( control, rigjoint )
			
			if( lastcontrol ) :
				pm.parentConstraint( lastcontrol, control.zero_group(), mo=True )
				# pm.pointConstraint( lastcontrol, control, mo=True )
				# pm.orientConstraint( lastcontrol, control, mo=True )
			lastcontrol = control
			
			self.add_child( control )

		return True

	def addinSquashStretch( self ) :
		controlsrigjointszipped = zip( 
			self.tree_children( 'rigControl' ),
			self.tree_children( 'jointchain' )[0].rigjoints
		)

		for control, rigjoint in controlsrigjointszipped :
			alljoints = [ rigjoint ] + self.tree_children( 'jointchain' )[0].minorrigjoints[ rigjoint ]
			for joint in alljoints :
				primaryaxis = joint.getRotationOrder()[0].upper()
				controlscaleattr = control.attr( 'scale' + primaryaxis )			
				controlscaleattr >> joint.attr( 'scale' + primaryaxis )
				
				# multdiv to create volume preservation
				multdiv = pm.nodetypes.MultiplyDivide()
				multdiv.rename( utils.name_from_tags( rigjoint, 'squashstretch', 'multiplydivide' ) )
				multdiv.operation.set( 2 )
				multdiv.input1X.set( 1 )
				controlscaleattr >> multdiv.input2X
				multdiv.outputX >> joint.attr( 'scale' + joint.getRotationOrder()[1].upper() )
				multdiv.outputX >> joint.attr( 'scale' + joint.getRotationOrder()[2].upper() )

				return True

	def addinDistributedTwist( self ) :
		pass



class IkRig( BasicRig ) :
	PARTNAME = 'ikRig'

	# def __init__( self ) :
	# 	super( IkRig, self ).__init__()

	def create( self, _jointchain=None ) :
		super( IkRig, self ).create( _jointchain )

		jointchains = self.tree_children( 'jointchain' )
		if( len( jointchains ) != 1 ) :
			utils.err( 'IkRig children includes more than ONE jointchain. Not sure which to use. Skipping...' )
			return False
		
		simplejointchain = jointchains[0].duplicate_jointchain( self.PARTNAME, 'driver', _simple=True )
		self.add_child( simplejointchain )

		numjoints = len( simplejointchain.rigjoints )
		startjoint = simplejointchain.rigjoints[0]
		middlejoint = simplejointchain.rigjoints[ numjoints / 2 ]
		endjoint = simplejointchain.rigjoints[-1]

		# create ik handle
		ikcontrolname = utils.name_from_tags( self.tree_root().name, 'ik' )
		ikcontrol = controls.RigControl( n=ikcontrolname )
		ikcontrol.position_to_object( endjoint )
		self.add_child( ikcontrol )

		ikhandlename = utils.name_from_tags( endjoint, 'ikhandle' )
		ikhandle, ikeffector = pm.ikHandle( 
			startjoint, 
			endjoint,
			solver='ikRPsolver',
			endEffector=endjoint,
			name=ikhandlename
		)
		ikeffector.rename( utils.name_from_tags( endjoint, 'ikeffector' ) )
		self.add_child( ikhandle )


		# parent endjoint to ikcontrol
		pm.pointConstraint( ikcontrol, ikhandle )
		pm.orientConstraint( ikcontrol, endjoint )

		# create polevector
		pvcontrolname = utils.name_from_tags( self.tree_root().name, 'polevector' )
		pvcontrol = controls.RigControl( n=pvcontrolname )
		self.add_child( pvcontrol )

		# position in center of jointchain
		pm.delete( pm.pointConstraint( 
			simplejointchain.rigjoints + [ pvcontrol.zero_group() ]
		) )
		# aim towards middle joint and move
		pm.delete( pm.aimConstraint(
			[ middlejoint, pvcontrol.zero_group() ],
			wut='object',
			wuo=middlejoint.getParent()
		) )
		pvcontrol.sdk_group().translateBy( ( 3, 0, 0 ) )

		# create the pv constraint
		pm.poleVectorConstraint( 
			[ pvcontrol, ikhandle ]
		)

		# connect jointchain to simplejointchain
		try :
			jointchainzipped = zip(
				jointchains[0].rigjoints,
				simplejointchain.rigjoints
			)
		except :
			utils.err( '%s and %s have different numbers of rigjoints. Not attempting to connect.' )
			return False

		for j in jointchainzipped :
			pm.parentConstraint( [ j[1], j[0] ], mo=False )

		return True


	def addinSquashStretch( self ) :
		jointchain = self.tree_children( 'jointchain' )[0]
		control = self.tree_children( 'rigControl' )[0]

		length = jointchain.length_between( 0, len( jointchain.rigjoints ) )
		distancebetween = pm.nodetypes.DistanceBetween()

		jointchain.rigjoints[0].worldMatrix >> distancebetween.inMatrix1
		jointchain.rigjoints[0].rotatePivotTranslate >> distancebetween.point1
		control.worldMatrix >> distancebetween.inMatrix2
		control.rotatePivotTranslate >> distancebetween.point2

		multdiv = pm.nodetypes.MultiplyDivide()
		multdiv.rename( utils.name_from_tags( control, 'squashstretch', 'multiplydivide' ) )	
		multdiv.operation.set( 2 )
		
		multdiv.input2X.set( length )
		distancebetween.distance >> multdiv.input1X

		alljoints = self.tree_children( 'jointchain' )[0].all_joints()
		for joint in alljoints :
			primaryaxis = joint.getRotationOrder()[0].upper()
			multdiv.outputX >> joint.attr( 'scale' + primaryaxis )




class IkFkBlendRig( BlendRig ) :
	PARTNAME = 'ikfkBlendRig'

	def __init__( self ) :
		pass

	def create( self, _jointchain=None ) :
		pass

		