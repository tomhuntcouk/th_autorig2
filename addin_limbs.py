import pymel.all as pm

from tree import TreeNode
import utils

class BaseAddin( TreeNode ) :
	PARTNAME = 'BaseAddin'
	AFFECTEDATTRS = []

	def __init__( self ) :
		super( BaseAddin, self ).__init__()

	def create( self ) :
		pass



class DistributedTwistAddin( BaseAddin ) :
	PARTNAME = 'distributedTwistAddin'
	AFFECTEDATTRS = [
		'rotateX',
		'rotateY',
		'rotateZ',
	]

	def __init__( self, _primaryaxis='x' ) :
		super( DistributedTwistAddin, self ).__init__()
		_primaryaxis = _primaryaxis.lower().replace( 'rotate', '' )
		_primaryaxis = _primaryaxis.upper()
		self.primaryaxis = _primaryaxis
		self.transformation = 'rotate'

	def create( self ) :
		# distribute the twist along the axis of each major joint
		# amongst the minor joints above it

		attribute = self.transformation + self.primaryaxis
		if( attribute not in self.AFFECTEDATTRS ) :
			utils.err( '%s not in DistributedTwistAddin.AFFECTEDATTRS. Skipping...' % ( self.primaryaxis ) )
			return False

		rig = self.tree_parent()
		jointchains = rig.tree_children( 'jointchain' )		

		for jointchain in jointchains :

			for i, rigjoint in enumerate( jointchain.rigjoints ) :			
				# leave the last in the jointchain as it is guaranteed to not have any minorjoints
				# before it to share its rotation with
				if( i == 0 ) : continue

				if( rigjoint not in jointchain.minorrigjoints.keys() ) :
					continue

				# # WARNING
				# # this way of getting the control (or top level controlling transform)
				# # is likely to not be accurate - a better way needs to be found
				control = None
				for transform in rigjoint.listHistory( type='transform' ) :
					if( transform.getShape() ) :
						control = transform
						break

				if( not control ) :
					continue
				
				minorjoints = jointchain.minorrigjoints[ jointchain.rigjoints[ i - 1 ] ]

				# create a multdiv to temper control's rotation by 1/len(minorjoints)
				multdiv = pm.nodetypes.MultiplyDivide( n=utils.name_from_tags( 
					rigjoint, 'rotateaddin', 'multiplydivide',
					_replacelast=False
				) )
				factor = 1.0 / ( len( minorjoints ) + 1 )
				multdiv.input2.set( [factor] * 3 )
				control.attr( attribute ) >> multdiv.attr( 'input1' + self.primaryaxis )

				# connect the multdiv to rigjoint and minorjoints
				for joint in [ rigjoint ] + minorjoints :
					multdiv.attr( 'output' + self.primaryaxis ) >> joint.attr( attribute )
				


class SquashStretchChainAddin( BaseAddin )
	PARTNAME = 'distributedTwistAddin'
	AFFECTEDATTRS = [
		'scaleX',
		'scaleY',
		'scaleZ',
	]

	def __init__( self, _primaryaxis='x' ) :
		super( DistributedTwistAddin, self ).__init__()
		_primaryaxis = _primaryaxis.lower().replace( 'rotate', '' )
		_primaryaxis = _primaryaxis.upper()
		self.primaryaxis = _primaryaxis
		self.transformation = 'rotate'




