import pymel.all as pm

from tree import TreeNode
import utils, settings


class RelevantObjects( object ) :
	def __init__( self, _jointchain, _rigjoint, _minorrigjoints, _control ) :
		super( RelevantObjects, self ).__init__()
		self.jointchain = _jointchain
		self.rigjoint = _rigjoint
		self.minorrigjoints = _minorrigjoints
		self.control = _control



class BaseAddin( TreeNode ) :
	PARTNAME = 'BaseAddin'
	AFFECTEDATTR = ''

	def __init__( self ) :
		super( BaseAddin, self ).__init__()
		self.attribute = ''
		self.jointchains = None

	def relevant_objects_generator( self, _jointchains ) :
		for jointchain in _jointchains :
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

				yield RelevantObjects( jointchain, rigjoint, minorjoints, control )

	def create( self ) :
		self.attribute = self.transformation + self.primaryaxis
		# if( attribute not in self.AFFECTEDATTRS ) :
		# 	utils.err( '%s not in DistributedTwistAddin.AFFECTEDATTRS. Skipping...' % ( self.primaryaxis ) )
		# 	return False
		self.jointchains = self.tree_parent().tree_children( 'jointchain' )



class DistributedTwistAddin( BaseAddin ) :
	PARTNAME = 'distributedTwistAddin'
	AFFECTEDATTR = 'rotate'

	def __init__( self, _primaryaxis=None ) :
		super( DistributedTwistAddin, self ).__init__()
		if not _primaryaxis :
			_primaryaxis = settings.rotationorder[0].upper()
		self.primaryaxis = _primaryaxis
		self.transformation = self.AFFECTEDATTR

	def create( self ) :
		# distribute the twist along the axis of each major joint
		# amongst the minor joints above it
		super( DistributedTwistAddin, self ).create()
		
		for relevantobject in self.relevant_objects_generator( self.jointchains ) :
			# create a multdiv to temper control's rotation by 1/len(minorjoints)
			multdiv = pm.nodetypes.MultiplyDivide( n=utils.name_from_tags( 
				relevantobject.rigjoint, 'rotateaddin', 'multiplydivide',
				_replacelast=False
			) )
			factor = 1.0 / ( len( relevantobject.minorrigjoints ) + 1 )
			multdiv.input2.set( [factor] * 3 )
			relevantobject.control.attr( self.attribute ) >> multdiv.attr( 'input1' + self.primaryaxis )

			# connect the multdiv to rigjoint and minorjoints
			for joint in [ relevantobject.rigjoint ] + relevantobject.minorrigjoints :
				multdiv.attr( 'output' + self.primaryaxis ) >> joint.attr( self.attribute )


				

class SquashStretchChainAddin( BaseAddin ) :
	PARTNAME = 'squashStretchChainAddin'
	AFFECTEDATTR = 'scale'

	def __init__( self, _primaryaxis=None ) :
		super( SquashStretchChainAddin, self ).__init__()
		if not _primaryaxis :
			_primaryaxis = settings.rotationorder[0].upper()
		self.primaryaxis = _primaryaxis
		self.transformation = self.AFFECTEDATTR

	def create( self ) :
		# for each control
		# distance between last joint with a control / fist joint if there is none
		# get distance between last/first joint
		# distance between node
		# if distnace between node > distance
		# scale each joint (including minorjoints) along primary axis

		super( SquashStretchChainAddin, self ).create()

		for relevantobject in self.relevant_objects_generator( self.jointchains ) :
			print relevantobject.control




class NoFlipPoleVectorAddin( BaseAddin ) :
	pass


