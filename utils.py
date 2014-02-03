import pymel.all as pm

import os
import inspect

should_error = False

__dataattrdict = {
	'str'	: 'dt="string"'
}


def err( _message ) :
	caller = inspect.currentframe()
	caller = inspect.getouterframes( caller, 2 )
	caller = caller[1][1].split( os.sep )[-1] + ' : ' + caller[1][3]
	
	_message = caller + ' : ' + _message

	if( should_error ) : pm.error( _message )
	else : pm.warning( _message )


def add_set_attr( _obj, _attr, _value ) :
	if( not _obj.hasAttr( _attr ) ) :
		t = type( _value ).__name__
		eval( '_obj.addAttr( _attr, %s )' % ( __dataattrdict[ t ] ) )
	try :
		_obj.setAttr( _attr, _value )
		return True
	except AttributeError :
		err( 'value of %s cannot be applied to %s attr %s.%s' % ( _value, _obj.getAttr( _attr, type=True ), _obj, _attr ) )
		return False