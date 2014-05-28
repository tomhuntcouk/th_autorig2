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

			utils.create_zero_sdk_groups( ribbon )

			# continue
			

			# cluster start, mid and end of curve
			# startcluster = pm.cluster( curve.cv[0:1], name=utils.name_from_tags( rigjoint1, 'start', 'cluster') )[1]
			# midcluster = pm.cluster( curve.cv[2], name=utils.name_from_tags( rigjoint1, 'mid', 'cluster' ) )[1]
			# endcluster = pm.cluster( curve.cv[-2:], name=utils.name_from_tags( rigjoint1, 'end', 'cluster' ) )[1]

			startcluster = pm.cluster( 	ribbon.cv[0:1][0:1], name=utils.name_from_tags( rigjoint1, 'start', 'cluster') )[1]
			midcluster = pm.cluster( 	ribbon.cv[2][0:1], name=utils.name_from_tags( rigjoint1, 'mid', 'cluster' ) )[1]
			endcluster = pm.cluster( 	ribbon.cv[-2:][0:1], name=utils.name_from_tags( rigjoint1, 'end', 'cluster' ) )[1]

			# pm.group( startcluster, midcluster, endcluster )

			# pm.delete( pm.parentConstraint( [ rigjoint1, startcluster ], mo=False ) )
			# pm.delete( pm.parentConstraint( [ rigjoint2, startcluster ], mo=False ) )

			# continue

			# parent clusters to respective rigjoints
			pm.parentConstraint( [ rigjoint1, startcluster ], mo=False )
			pm.parentConstraint( [ rigjoint2, endcluster ], mo=False )

			# group then point/parent constrain middle cluster to end clusters
			sdkgroup, zerogroup = utils.create_zero_sdk_groups( midcluster )
			zerogroup.setRotation( rigjoint1.getRotation( space='world' ), space='world' )
			pm.pointConstraint( [ rigjoint1, rigjoint2, zerogroup ], mo=False )
			pm.orientConstraint( [ rigjoint1, zerogroup ], mo=False )

			# continue


			jointsToAttachToCurve = [ jointchain.rigjoints[i] ]
			jointsToAttachToCurve += jointchain.minorrigjoints[ jointsToAttachToCurve[0] ]
			jointsToAttachToCurve += [ jointchain.rigjoints[i+1] ]

			# ik = pm.ikHandle(
			# 	solver='ikSplineSolver',
			# 	createCurve=False,
			# 	curve=curve,
			# 	startJoint=jointsToAttachToCurve[0],
			# 	endEffector=jointsToAttachToCurve[-1]
			# )

			# continue

			# locator for aim up
			# loc = pm.spaceLocator()
			# pm.parent( loc, rigjoint1 )
			# loc.setRotation( (0,0,0) )
			# loc.setTranslation( (1,2,0) )


			for rigjoint in jointsToAttachToCurve :

				# u = pm.api.SafeApiPtr( 0.0 )
				# v = pm.api.SafeApiPtr( 0.0 )

				p = rigjoint.getTranslation( space='world' )
				posi = pm.nodetypes.ClosestPointOnSurface()
				ribbon.worldSpace >> posi.inputSurface
				posi.inPosition.set( p )
				u = posi.u.get()
				v = posi.v.get()

				pm.delete( posi )

				follicle = pm.nodetypes.Follicle()
				ribbon.local >> follicle.inputSurface
				ribbon.worldMatrix[0] >> follicle.inputWorldMatrix
				follicle.parameterU.set( u )
				follicle.parameterV.set( v )

				# print closestPoint

				# # 	closestpointoncurve node - get closest param
				# closestPoint = curve.closestPoint( rigjoint.getTranslation( space='world' ), space='world' )
				# closestParam = curve.getParamAtPoint( closestPoint, space='world' )

				# # 	curveInfoNode - get world pos of closest param
				# curveInfoNode = pm.nodetypes.PointOnCurveInfo()
				# curve.getShape().worldSpace >> curveInfoNode.inputCurve
				# curveInfoNode.parameter.set( closestParam )

				# #	decompose then recompose matrix to attach joint to curve
				
				# null = pm.group( empty=True )
				# curveInfoNode.position >> null.translate
				# pm.tangentConstraint(
				# 	[ curve, null ],
				# 	worldUpType='objectrotation',
				# 	worldUpObject=loc
				# )




				# pm.pointConstraint( [ null, rigjoint ], mo=False )
				# pm.orientConstraint( [ null, rigjoint ], mo=False )




				# # some kind of normal constraint to create twist

				# tc = pm.tangentConstraint( [ curve, rigjoint ] )
				# pm.orientConstraint( [ null, rigjoint ], mo=False )

				# cp1 = pm.nodetypes.VectorProduct()
				# cp1.operation.set( 2 )
				# cp2 = pm.nodetypes.VectorProduct()
				# cp2.operation.set( 2 )
				# fbfm = pm.nodetypes.FourByFourMatrix()

				# curveInfoNode.tangent >> cp1.input1
				# curveInfoNode.tangent >> cp2.input1
				# cp1.output >> cp2.input2

				# cp1.outputX >> fbfm.



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

		