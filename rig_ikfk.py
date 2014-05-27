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
		
		for i in range( len( simplejointchain.rigjoints ) - 1 ) :
			# create a curve between each pair of simple rigjoints
			rigjoint1 = simplejointchain.rigjoints[i]
			rigjoint2 = simplejointchain.rigjoints[i+1]

			curve = pm.curve( degree=1, point=[
				rigjoint1.getTranslation( space='world' ),
				rigjoint2.getTranslation( space='world' )				
			], name=utils.name_from_tags( rigjoint1, 'curve' ) )

			# rebuild with numspan 2 and 3 degree
			pm.rebuildCurve( curve, degree=3, spans=2 )

			# move vtx[1] and vtx[-2] to respective ends of curve		
			curve.cv[1].setPosition( curve.cv[0].getPosition( space='world' ), space='world' )
			curve.cv[-2].setPosition( curve.cv[-1].getPosition( space='world' ), space='world' )

			# cluster start, mid and end of curve
			startcluster = pm.cluster( curve.cv[0:1], name=utils.name_from_tags( rigjoint1, 'start', 'cluster') )[1]
			midcluster = pm.cluster( curve.cv[2], name=utils.name_from_tags( rigjoint1, 'mid', 'cluster' ) )[1]
			endcluster = pm.cluster( curve.cv[-2:], name=utils.name_from_tags( rigjoint1, 'end', 'cluster' ) )[1]

			# parent clusters to respective rigjoints
			pm.parentConstraint( [ rigjoint1, startcluster ], mo=False )
			pm.parentConstraint( [ rigjoint2, endcluster ], mo=False )

			# group then point/parent constrain middle cluster to end clusters
			sdkgroup, zerogroup = utils.create_zero_sdk_groups( midcluster )
			zerogroup.setRotation( rigjoint1.getRotation( space='world' ), space='world' )
			pm.pointConstraint( [ rigjoint1, rigjoint2, zerogroup ], mo=False )

			jointsToAttachToCurve = [ jointchain.rigjoints[i] ]
			jointsToAttachToCurve += jointchain.minorrigjoints[ jointsToAttachToCurve[0] ]
			jointsToAttachToCurve += [ jointchain.rigjoints[i+1] ]
			for rigjoint in jointsToAttachToCurve :
				# 	closestpointoncurve node - get closest param
				closestPoint = curve.closestPoint( rigjoint.getTranslation( space='world' ), space='world' )
				closestParam = curve.getParamAtPoint( closestPoint, space='world' )

				# 	curveInfoNode - get world pos of closest param
				curveInfoNode = pm.nodetypes.PointOnCurveInfo()
				curve.getShape().worldSpace >> curveInfoNode.inputCurve
				curveInfoNode.parameter.set( closestParam )

				#	decompose then recompose matrix to attach joint to curve
				
				null = pm.group( empty=True )
				curveInfoNode.position >> null.translate
				pm.pointConstraint( [ null, rigjoint ], mo=False )


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

		