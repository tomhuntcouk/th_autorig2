import pymel.all as pm

from virtual import BaseVirtual

import utils, settings



class RigJoint( BaseVirtual, pm.Joint ) :
	PARTNAME = 'RigJoint'

	def duplicate( self, simple=False, *args, **kwargs ) :	
		duplicatejoints = super( RigJoint, self ).duplicate( *args, **kwargs )
		if( simple ) :
			duplicatejoints = [ duplicatejoints.pop(0) ]
			duplicatejoints[0].setParent( None )
			duplicatejointchildren = duplicatejoints[0].getChildren()
			if( len( duplicatejointchildren ) ) :
				pm.delete( duplicatejointchildren )
		return duplicatejoints[0]


	def orient( self, orientchildless=True, rotationorder=None ) :
		# get the rotation order
		if( not rotationorder ) : rotationorder = settings.rotationorder

		# check we have a child to aim to and decide on aim vectors
		aimvector, upvector = utils.aim_axis_to_vectors( rotationorder )

		# if no children make aimvector is inverse of joint direction
		children = self.getChildren()
		parent = self.getParent()
		if( not parent ) : parent = self
		if( len( children ) < 1 ) :
			if( not orientchildless ) :
				utils.wrn( '%s has no children. Skipping orient...' % ( self.name() ) )
				return False
			else :
				aimvector = [ a * b for a, b in zip( aimvector, [-1] * 3 ) ]

		pm.select([])

		# create children average aim loc
		childrenlocator = pm.spaceLocator()
		if( len( children ) ) :			
			pm.delete( pm.pointConstraint( children + [ childrenlocator ], mo=False ) )
		else :
			childrenlocator.setTranslation( parent.getTranslation( space='world' ), space='world' )

		# create up aim loc and aim self towards it
		uplocator = pm.spaceLocator()
		pm.delete( pm.pointConstraint( [ parent, self, childrenlocator, uplocator ], mo=False ) )
		pm.delete( pm.aimConstraint( [ self, uplocator ], mo=False, wut='object', wuo=parent ) )
		uplocator.translateBy( ( 0, 0, 0.5 ) )

		# unparent children, aim the joint to the average of it's children, then reparent children
		for joint in children : joint.setParent( None )
		pm.delete( pm.aimConstraint( 
			[ childrenlocator, self ],
			mo=False,
			wut='object',
			wuo=uplocator,
			upVector=upvector,
			aim=aimvector
		) )
		pm.makeIdentity( self, a=True, r=True )
		for joint in children : joint.setParent( self )

		# tidy up
		pm.delete( childrenlocator )
		pm.delete( uplocator )
		pm.select( self )

		return True

	def split( self, numsplits ) :
		# check self has only one child
		children = self.getChildren()
		if( not children or len( children ) != 1 ) :
			utils.err( '%s does not have exactly ONE child. Skipping split...' % ( self.name() ) )
			return False
		child = children[0]

		# unparent child
		child.setParent( None )
		pm.select( None )

		# get position of self and child
		selfpos = self.getTranslation( space='world' )
		childpos = child.getTranslation( space='world' )
		# selfpos = pm.xform( self, q=True, translation=True, worldSpace=True )
		# childpos = pm.xform( child, q=True, translation=True, worldSpace=True )

		# first unparent self and store parent
		parent = self.getParent()
		self.setParent( None )

		# create joints by lerping between selfpos and childpos
		splitjoints = []
		lastjoint = self
		for i in range( 1, numsplits + 1 ) :
			t = i * ( 1.0 / ( numsplits + 1 ) )
			newjointpos = utils.lerp( selfpos, childpos, t )
			
			pm.select( None )
			newjoint = lastjoint.duplicate( n=utils.renumber_from_name( self.name(), i ), simple=True )
			newjoint.setTranslation( newjointpos, space='world' )
			
			splitjoints.append( newjoint )
			newjoint.setParent( lastjoint )
			lastjoint = newjoint
		child.setParent( lastjoint )

		self.setParent( parent )
		pm.select( self )
		return splitjoints


