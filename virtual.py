import pymel.all as pm

import settings, utils


class BaseVirtual() :
	PARTNAME = 'baseVirtual'

	@classmethod
	def __recurse_bases( cls, _base ) :
		bases = list( cls.__bases__ )
		for base in bases :
			bases.extend( cls.__recurse_bases( base ) )
		return bases
			

	@classmethod
	def get_pynodetype( cls ) :
		for base in utils.get_full_class_inheritance( cls ) :
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
		pynodetype = cls.get_pynodetype()
		if( pynodetype ) : 
			node = pynodetype( **kwargs )
			return node.name()
		else : 
			utils.err( 'No PyNode found in bases of %s' % ( cls.__name__ ) )
			return False

	@classmethod
	def _postCreateVirtual( cls, node, **kwargs ) :
		# print '-----------', '_postCreateVirtual', node
		node = pm.PyNode( node )
		utils.add_set_attr( node, settings.attrname, cls.PARTNAME )

	def set( self, _name, _value ) :		
		self.__dict__[ _name ] = _value
		try :
			utils.add_set_attr( self, _name, _value )
		except :
			pass

	def get( self, _name ) :
		ret = None
		try :
			ret = self.getAttr( _name )
		except :
			ret = self.getattr( _name )

		try : return pm.PyNode( ret )
		except : return ret



# pm.factories.registerVirtualClass( BaseVirtual, nameRequired=False )
