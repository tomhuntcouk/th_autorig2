import pymel.all as pm
import utils
import inspect

attrname = 'th_autorig_nodecheck'

class BaseJoint( pm.Joint ) :
	nodeType = 'BaseJoint'

	@classmethod
	def convert_to_virtual( cls, _joint ) :
		print type( _joint )
		if( type( _joint ) == pm.Joint ) :
			if utils.add_set_attr( _joint, attrname, cls.nodeType ) :
				return True
			else :
				return False
		else :		
			utils.err( '%s is not a joint' % ( _joint.name() ) )	
			return False

	@classmethod
	def _isVirtual( cls, obj, name ) :
		# print '--------', obj
		# print inspect.getmembers( obj.__getattribute__( 'fullPathName' ) )
		fn = pm.api.MFnDependencyNode( obj )
		try :
			if( fn.hasAttribute( attrname ) ) :
				plug = fn.findPlug( attrname )
				return plug.asString() == cls.nodeType
				# if( plug.asString() == cls.nodeType ) :
					# print plug.asString()
					# return True
				# return False
		except :
			pass
		return False

	@classmethod
	def _preCreateVirtual( cls, **kwargs ) :
		print 'pre'
		return kwargs

	@classmethod
	def _postCreateVirtual( cls, node ) :
		print 'post'
		node.addAttr( attrname, dt='string' )
		node.setAttr( attrname, cls.nodeType )


class RigJoint( BaseJoint ) :
	nodeType = 'RigJoint'

# pm.factories.registerVirtualClass( BaseJoint, nameRequired=False )
pm.factories.registerVirtualClass( RigJoint, nameRequired=False )



