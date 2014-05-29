import pymel.all as pm

import settings, utils


class BaseVirtual() :
	PARTNAME = 'baseVirtual'

	@classmethod
	def get_pynodetype( cls ) :
		for base in cls.__bases__ :
			if( base.__module__ == 'pymel.core.nodetypes' ) :
				return base
		return None

	@classmethod
	def convert( cls, obj ) :
		pynodetype = cls.get_pynodetype()
		if( type( obj ) == pynodetype ) :
			return utils.add_set_attr( obj, settings.attrname, cls.PARTNAME, keyable=False, locked=True )
		else :		
			utils.err( '%s is not a %s' % ( obj.name(), pynodetype ) )
			return False

	@classmethod
	def _isVirtual( cls, obj, name ) :
		# print '-----------', '_isVirtual'
		fn = pm.api.MFnDependencyNode( obj )
		try :			
			if( fn.hasAttribute( settings.attrname ) ) :				
				plug = fn.findPlug( settings.attrname )				
				return plug.asString() == cls.PARTNAME
		except :
			pass
		return False

	@classmethod
	def _preCreateVirtual( cls, **kwargs ) :
		# print '_preCreateVirtual'
		if 'n' in kwargs :
			name = kwargs.pop( 'n' )
		elif 'name' in kwargs :
			name = kwargs.get( 'name' )
		else :
			name = cls.PARTNAME
		kwargs[ 'name' ] = name
		pkwargs = {}		
		return kwargs, pkwargs

	@classmethod
	def _createVirtual( cls, **kwargs ) :
		# print '-----------', 'createVirtual'
		node = cls.get_pynodetype()( **kwargs )
		return node.name()

	@classmethod
	def _postCreateVirtual( cls, node, **kwargs ) :
		# print '-----------', '_postCreateVirtual', node
		node = pm.PyNode( node )
		utils.add_set_attr( node, settings.attrname, cls.PARTNAME )



# pm.factories.registerVirtualClass( BaseVirtual, nameRequired=False )
