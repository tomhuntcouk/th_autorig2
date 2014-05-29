import pymel.all as pm

from rig_basic import *
import controls
import utils, settings


class FkRig( BasicRig ) :
	PARTNAME = 'fkRig'

	# def __init__( self ) :
	# 	super( FkRig, self ).__init__()

	def create( self, _jointchain=None ) :
		super( FkRig, self ).create( _jointchain )
		
		return True

	def addinSquashStretch( self ) :
		pass

	def addinDistributedTwist( self ) :
		pass



class IkRig( BasicRig ) :
	PARTNAME = 'ikRig'

	def create( self, _jointchain=None ) :
		super( IkRig, self ).create( _jointchain )

		jointchains = self.tree_children( 'jointchain' )
		if( len( jointchains ) != 1 ) :
			utils.err( 'IkRig children includes more than ONE jointchain. Not sure which to use. Skipping...' )
			return False		

		jointchain = jointchains[0]

		# create a simple joint chain
		simplejointchain = jointchain.duplicate_jointchain( self.PARTNAME, 'driver', _simple=True )
		self.add_child( simplejointchain )
		
		pm.PyNode( 'leftUpperArm_1_IKJ_DRIVER' ).hide()
		pm.PyNode( 'leftUpperArm_1_j' ).hide()

		for i in range( len( simplejointchain.rigjoints ) - 1 ) :
			# create a curve between each pair of simple rigjoints
			rigjoint1 = simplejointchain.rigjoints[i]
			rigjoint2 = simplejointchain.rigjoints[i+1]

			v1 = pm.datatypes.Vector( rigjoint1.getTranslation( space='world' ) )
			v2 = pm.datatypes.Vector( rigjoint2.getTranslation( space='world' ) )
			curvelength = float( v1.distanceTo( v2 ) )

			dirvector = [ a * b for a, b in zip( 
				( curvelength, curvelength, curvelength ),
				utils.aim_axis_to_vectors( settings.rotationorder )[0]
			) ]

			curve = pm.curve( degree=1, point=[
				( 0, 0, 0 ),
				dirvector
				# v1, v2
			], name=utils.name_from_tags( rigjoint1, 'curve' ) )

			# rebuild with numspan 2 and 3 degree
			pm.rebuildCurve( curve, degree=3, spans=2 )

			# move vtx[1] and vtx[-2] to respective ends of curve		
			curve.cv[1].setPosition( curve.cv[0].getPosition( space='world' ), space='world' )
			curve.cv[-2].setPosition( curve.cv[-1].getPosition( space='world' ), space='world' )

			ribbonlength = 0.2

			ribbon = pm.extrude(
				curve,
				polygon=0,
				useProfileNormal=1,
				extrudeType=0,
				length=ribbonlength,
				ch=False,
				name=utils.name_from_tags( rigjoint1, 'nurbs' )
			)[0]

			ribbon.setTranslation( ( 0, 0, -(ribbonlength)/2 ) )
			ribbon.setPivots( ( 0, 0, 0 ), worldSpace=True )
			pm.makeIdentity( ribbon, apply=True )
			pm.delete( ribbon, ch=True )
			pm.delete( curve )

			utils.create_zero_sdk_groups( ribbon, _replacelast=False )

			startcluster = pm.cluster( 	ribbon.cv[0:1][0:1], name=utils.name_from_tags( rigjoint1, 'start', 'cluster') )[1]
			midcluster = pm.cluster( 	ribbon.cv[2][0:1], name=utils.name_from_tags( rigjoint1, 'mid', 'cluster' ) )[1]
			endcluster = pm.cluster( 	ribbon.cv[-2:][0:1], name=utils.name_from_tags( rigjoint1, 'end', 'cluster' ) )[1]

			# parent clusters to respective rigjoints
			pm.parentConstraint( [ rigjoint1, startcluster ], mo=False )
			pm.parentConstraint( [ rigjoint2, endcluster ], mo=False )

			# group then point/parent constrain middle cluster to end clusters
			sdkgroup, zerogroup = utils.create_zero_sdk_groups( midcluster, _replacelast=False )
			zerogroup.setRotation( rigjoint1.getRotation( space='world' ), space='world' )
			pm.pointConstraint( [ rigjoint1, rigjoint2, zerogroup ], mo=False )
			pm.orientConstraint( [ rigjoint1, zerogroup ], mo=False )

			jointsToAttachToCurve = [ jointchain.rigjoints[i] ]
			jointsToAttachToCurve += jointchain.minorrigjoints[ jointsToAttachToCurve[0] ]
			jointsToAttachToCurve += [ jointchain.rigjoints[i+1] ]

	
			for rigjoint in jointsToAttachToCurve :

				p = rigjoint.getTranslation( space='world' )
				posi = pm.nodetypes.ClosestPointOnSurface()
				ribbon.worldSpace >> posi.inputSurface
				posi.inPosition.set( p )
				u = min( max( posi.u.get(), 0.001 ), 0.999 )
				v = min( max( posi.v.get(), 0.001 ), 0.999 )

				pm.delete( posi )

				follicleshape = pm.nodetypes.Follicle()
				ribbon.local >> follicleshape.inputSurface
				ribbon.worldMatrix[0] >> follicleshape.inputWorldMatrix
				follicleshape.parameterU.set( u )
				follicleshape.parameterV.set( v )
				
				follicle = follicleshape.getParent()
				follicle.rename( utils.name_from_tags( rigjoint, 'follicle' ) )
				follicleshape.rename( follicle.name() + 'Shape' )

				follicleshape.outRotate >> follicle.rotate
				follicleshape.outTranslate >> follicle.translate

				# remove any constraints already on the joint
				pm.delete( rigjoint.getChildren( type='constraint' ) )

				pm.parentConstraint( [ follicle, rigjoint ], mo=True )
				

		return True
		


	def addinSquashStretch( self ) :
		pass

	def addinDistributedTwist( self ) :
		pass
		

class IkFkBlendRig( BlendRig ) :
	PARTNAME = 'ikfkBlendRig'

	def __init__( self ) :
		pass

	def create( self, _jointchain=None ) :
		pass

		