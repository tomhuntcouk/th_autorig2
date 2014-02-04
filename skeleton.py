import pymel.all as pm
import utils
import inspect

import settings

"""
to fix __apicls__ error i had to add __apicls__ to validSpecialAttrs in
pm.factories.VirtualClassManager.register()

ideally this should be fixed without directly modifying core
"""

# print pm.factories.VirtualClassManager.register


class BaseJoint( pm.Joint ) :
	nodeType = 'BaseJoint'

	@classmethod
	def convert_to_virtual( cls, _joint ) :
		if( type( _joint ) == pm.Joint ) :
			return utils.add_set_attr( _joint, settings.attrname, cls.nodeType )
		else :		
			utils.err( '%s is not a joint' % ( _joint.name() ) )	
			return False

	@classmethod
	def _isVirtual( cls, obj, name ) :
		print '_____', obj, name
		fn = pm.api.MFnDependencyNode( obj )
		try :
			if( fn.hasAttribute( settings.attrname ) ) :
				plug = fn.findPlug( settings.attrname )
				return plug.asString() == cls.nodeType
		except :
			pass
		return False

	@classmethod
	def _preCreateVirtual( cls, **kwargs ) :
		return kwargs

	@classmethod
	def _postCreateVirtual( cls, node ) :
		node.addAttr( settings.attrname, dt='string' )
		node.setAttr( settings.attrname, cls.nodeType )


class RigJoint( BaseJoint ) :
	nodeType = 'RigJoint'

	def orient( self ) :
		# check we have a child to aim to
		children = self.getChildren()
		parent = self.getParent()
		if( not parent ) : parent = self
		if( len( children ) < 1 ) :
			utils.wrn( '%s has no children. Skipping orient...' % ( self.name() ) )
			return False

		# create children average aim locator
		childrenlocator = pm.spaceLocator()
		pm.delete( pm.pointConstraint( children + [ childrenlocator ], mo=False ) )

		# create up aim locator
		uplocator = pm.spaceLocator()
		pm.delete( pm.pointConstraint( [ parent, self, childrenlocator, uplocator ], mo=False ) )
		pm.delete( pm.aimConstraint( [ self, uplocator ], mo=False, wut='object', wuo=parent ) )
		uplocator.translateBy( ( 0, 0, 0.5 ) )

		# unparent children, aim the joint to the average of it's children, then reparent children
		for joint in children : joint.setParent( None )
		pm.delete( pm.aimConstraint( [ childrenlocator, self ], mo=False, wut='object', wuo=uplocator ) )
		pm.makeIdentity( self, a=True, r=True )
		for joint in children : joint.setParent( self )

		# tidy up
		pm.delete( childrenlocator )
		pm.delete( uplocator )
		pm.select( self )

		return True


	def split( self, _numsplits ) :
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
		print self.getAttr( 'translate' )
		selfpos = self.getTranslation( space='world' )
		childpos = child.getTranslation( space='world' )

		# create joints by lerping between selfpos and childpos
		ret = []
		lastjoint = self
		for i in range( 1, _numsplits + 1 ) :
			t = i * ( 1.0 / ( _numsplits + 1 ) )
			newjointpos = utils.lerp( selfpos, childpos, t )
			newjoint = RigJoint( n=utils.renumber_from_name( self.name(), i ) )
			newjoint.setTranslation( newjointpos, space='world' )
			ret.append( newjoint )
			newjoint.setParent( lastjoint )
			lastjoint = newjoint
		child.setParent( lastjoint )

		pm.select( self )
		return ret


# pm.factories.registerVirtualClass( BaseJoint, nameRequired=False )
pm.factories.registerVirtualClass( RigJoint, nameRequired=False )



