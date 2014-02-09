import pymel.all as pm

import utils
import settings

"""
to fix __apicls__ error i had to add __apicls__ to validSpecialAttrs in
pm.factories.VirtualClassManager.register()

ideally this should be fixed without directly modifying core


the pymel shipped with Maya 2014 errors when trying to access any methods on any class inheriting from MFnDependencyNode
clone the PyMel Github repo to resolve the problem


"""

# print pm.factories.VirtualClassManager.register


class BaseJoint( pm.Joint ) :
	NODETYPE = 'BaseJoint'

	@classmethod
	def convert_to_virtual( cls, _joint ) :
		if( type( _joint ) == pm.Joint ) :
			return utils.add_set_attr( _joint, settings.attrname, cls.NODETYPE )
		else :		
			utils.err( '%s is not a joint' % ( _joint.name() ) )	
			return False

	@classmethod
	def _isVirtual( cls, obj, name ) :
		fn = pm.api.MFnDependencyNode( obj )
		try :
			if( fn.hasAttribute( settings.attrname ) ) :
				plug = fn.findPlug( settings.attrname )
				return plug.asString() == cls.NODETYPE
		except :
			pass
		return False

	@classmethod
	def _preCreateVirtual( cls, **kwargs ) :
		if 'n' in kwargs :
			name = kwargs.pop( 'n' )
		elif 'name' in kwargs :
			name = kwargs.get( 'name' )
		else :
			name = cls.NODETYPE
		kwargs[ 'name' ] = name
		return kwargs

	@classmethod
	def _postCreateVirtual( cls, node, **kwargs ) :
		node.addAttr( settings.attrname, dt='string' )
		node.setAttr( settings.attrname, cls.NODETYPE )


class RigJoint( BaseJoint ) :
	NODETYPE = 'RigJoint'

	def duplicate( self, *args, **kwargs ) :
		# duplicates the joint without children
		newrigjoints = super( RigJoint, self ).duplicate( *args, **kwargs )
		for newrigjoint in newrigjoints :
			newrigjoint.setParent( None )
			newrigjointchildren = newrigjoint.getChildren()
			if( len( newrigjointchildren ) ) :
				pm.delete( newrigjointchildren[0] )
		return newrigjoints

	def orient( self, _orientchildless=True ) :		
		# check we have a child to aim to
		aim = ( 1, 0, 0 )
		children = self.getChildren()
		parent = self.getParent()
		if( not parent ) : parent = self
		if( len( children ) < 1 ) :
			if( not _orientchildless ) :
				utils.wrn( '%s has no children. Skipping orient...' % ( self.name() ) )
				return False
			else :
				aim = ( -1, 0, 0 )			

		pm.select( None )

		# create children average aim locator
		childrenlocator = pm.spaceLocator()
		if( len( children ) ) :			
			pm.delete( pm.pointConstraint( children + [ childrenlocator ], mo=False ) )
		else :
			childrenlocator.setTranslation( parent.getTranslation( space='world' ), space='world' )

		# create up aim locator and aim self to it
		uplocator = pm.spaceLocator()
		pm.delete( pm.pointConstraint( [ parent, self, childrenlocator, uplocator ], mo=False ) )
		pm.delete( pm.aimConstraint( [ self, uplocator ], mo=False, wut='object', wuo=parent ) )
		uplocator.translateBy( ( 0, 0, 0.5 ) )

		# unparent children, aim the joint to the average of it's children, then reparent children
		for joint in children : joint.setParent( None )
		pm.delete( pm.aimConstraint( [ childrenlocator, self ], mo=False, wut='object', wuo=uplocator, aim=aim ) )
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
		selfpos = self.getTranslation( space='world' )
		childpos = child.getTranslation( space='world' )
		# selfpos = pm.xform( self, q=True, translation=True, worldSpace=True )
		# childpos = pm.xform( child, q=True, translation=True, worldSpace=True )

		# first unparent self and store parent
		parent = self.getParent()
		self.setParent( None )

		# create joints by lerping between selfpos and childpos
		ret = []
		lastjoint = self
		for i in range( 1, _numsplits + 1 ) :
			t = i * ( 1.0 / ( _numsplits + 1 ) )
			newjointpos = utils.lerp( selfpos, childpos, t )
			
			pm.select( None )
			newjoint = lastjoint.duplicate( n=utils.renumber_from_name( self.name(), i ) )[0]
			newjoint.setTranslation( newjointpos, space='world' )
			
			ret.append( newjoint )
			newjoint.setParent( lastjoint )
			lastjoint = newjoint
		child.setParent( lastjoint )

		self.setParent( parent )
		pm.select( self )
		return ret


# pm.factories.registerVirtualClass( BaseJoint, nameRequired=False )
pm.factories.registerVirtualClass( RigJoint, nameRequired=False )



