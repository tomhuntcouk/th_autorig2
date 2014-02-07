import pymel.all as pm

import os
import inspect

import settings

__dataattrdict = {
	'str'	: 'dt="string"'
}

__classdict = {
	None				: '',
	'FkRig'				: '_FKJ',
	'IkChainrig'		: '_IKJ',
	'BaseBlendrig'		: '_BJ',
	'Control'			: '_CNTRL',	
	'IkHandle'			: '_HND',
	'IkEffector'		: '_EFF',
	'AnimCurveUL'		: '_ACUL',
	'MultiplyDivide'	: '_MULTDIV',
	'PlusMinusAverage'	: '_PMA'
}

__tagdict = {
	None : 			'',		
	'sdk' : 		'_SDK',
	'zero' : 		'_ZERO',
	'ik' :			'_IK',
	'ikdriver' :	'_DRIVER',
	'fk' :			'_FK',
	'polevector' :	'_PV',
	'ikfkswitcher' : '_IKFK'
}

#########################################################
# debug
#########################################################


def _get_caller() :
	caller = inspect.currentframe()
	caller = inspect.getouterframes( caller, 2 )
	caller = caller[1][1].split( os.sep )[-1] + ' : ' + caller[1][3]
	return caller

def err( _message ) :	
	caller = _get_caller()
	_message = caller + ' : ' + _message
	if( settings.should_error ) : pm.error( _message )
	else : pm.warning( _message )

def wrn( _message ) :	
	caller = _get_caller()
	_message = caller + ' : ' + _message
	pm.warning( _message )


#########################################################
# attributes
#########################################################


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

def renumber_from_name( _name, _number ) :
	d = settings.name_string_delimeter
	namesplit = _name.rsplit( d, 1 )
	return '%s%s%s%s%s' % ( namesplit[0], d, _number, d, namesplit[1] )

def name_from_dict( _obj, _class=None, _tag=None ) :
	if not _class and not _tag : return _obj.name()
	namesplit = _obj.name().rsplit( '_', 1 )	
	ret = namesplit[0]
	if _tag : ret += settings.name_string_delimeter + __tagdict[ _tag ]
	if _class : ret += settings.name_string_delimeter + __classdict[ _class ]
	return ret


#########################################################
# math
#########################################################


def lerp( p1, p2, t ) :
	if( type( p1 ) == type( p2 ) ) :
		if( type( p1 ) == pm.datatypes.Vector ) :
			# calculate vector lerp			
			outVector = pm.datatypes.Vector( 0, 0, 0 )			
			for i in [ 'x', 'y', 'z' ] :				
				setattr( outVector, i, lerp( getattr( p1, i ), getattr( p2, i ), t ) )
			return outVector
		elif( type( p1 ) == list ) :
			# calculate list lerp
			outList = [ 0, 0, 0 ]
			for i, v in enumerate( p1 ) :
				outList[i] = lerp( p1[i], p2[i], t )
			return outList
		elif( type( p1 ) == float  ) :
			# calculate float lerp
			return p1 + ( p2 - p1 ) * t		
		else :
			err( 'inputs for lerp ( %s, %s ) not vector, list or float' % ( p1, p2 ) )
			return False
	else :
		err( 'inputs for lerp ( %s %s ) not of same type' % ( p1, p2 ) )
		return False

