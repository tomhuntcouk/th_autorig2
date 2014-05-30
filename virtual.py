import pymel.all as pm

try : import cPickle as pickle
except : import pickle

import settings, utils


class BaseVirtual() :
	PARTNAME = 'baseVirtual'

	__dataattrdict = {
		'str'	: 'dt="string"',
		'float' : 'at="float"',
		'list'	: 'dt="stringArray"'
	}

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
			# return utils.add_set_attr( obj, settings.attrname, cls.PARTNAME, _keyable=False, _locked=True )
			obj.addAttr( settings.attrname, dt='string' )
			obj.setAttr( settings.attrname, cls.PARTNAME )
			return True
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
		# utils.add_set_attr( node, settings.attrname, cls.PARTNAME )
		node.addAttr( settings.attrname, dt='string' )
		node.setAttr( settings.attrname, cls.PARTNAME )

	def is_attribute( self, _attr ) :
		return self.hasAttr( _attr )

	def set( self, _attr, _value ) :
		if( not self.hasAttr( _attr ) ) :
			# t = type( _value ).__name__		
			# cmd = '_obj.addAttr( _attr, %s, k=%s )' % ( __dataattrdict[ t ], _keyable )
			# eval( cmd )
			# let's try pickling everything into string attrs...
			self.addAttr( _attr, dt='string' )
		attr = pm.PyNode( '%s.%s' % ( self, _attr ) )
		attr.set( pickle.dumps( _value ) )

	def get( self, _attr ) :
		return pickle.loads( str( self.getAttr( _attr ) ) )

	def add_child( self, child ) :
		child.setParent( self )

	def children( self, rigtype=None ) :
		children = self.getChildren()
		if( rigtype ) :
			for i, child in enumerate( children ) :
				if type( child ).__name__ != rigtype :
					children.pop( i )
		return children

	# def set( self, _attr, _value ) :
	# 	# use this to set local variables
	# 	# if type(_attr) is in dict in utils.py it will be added as a maya attribute
	# 	try :
	# 		utils.add_set_attr( self, _attr, _value )
	# 	except :
	# 		print '%s is not added as an attribute' % ( _attr )
	# 		self.__dict__[ _attr ] = _value

	# def get( self, _attr ) :
	# 	ret = None
	# 	try :
	# 		ret = self.getAttr( _attr )
	# 	except :
	# 		ret = self.__dict__[ _attr ]

	# 	try : return pm.PyNode( ret )
	# 	except : return ret



# pm.factories.registerVirtualClass( BaseVirtual, nameRequired=False )
