import pymel.all as pm

import os
import inspect

import settings

__dataattrdict = {
	'str'	: 'dt="string"',
	'float' : 'at="float"',
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


def add_set_attr( _obj, _attr, _value, _locked=False, _keyable=True ) :	
	if( not _obj.hasAttr( _attr ) ) :
		t = type( _value ).__name__
		eval( '_obj.addAttr( _attr, %s, k=%s )' % ( __dataattrdict[ t ], _keyable ) )

	attr = pm.PyNode( '%s.%s' % ( _obj, _attr ) )	

	try :
		_obj.setAttr( _attr, _value )
		attr.setLocked( _locked )
		return attr
	except AttributeError :
		err( 'value of %s cannot be applied to %s attr %s.%s' % ( _value, _obj.getAttr( _attr, type=True ), _obj, _attr ) )
		return False

def renumber_from_name( _name, _number ) :
	d = settings.name_string_delimeter
	namesplit = _name.rsplit( d, 1 )
	try :
		name = '%s%s%s%s%s' % ( namesplit[0], d, _number, d, namesplit[1] )
		return name
	except :
		err( str(namesplit) )
		return False
	

def get_tag( _tag ) :
	return settings.tagdict[ _tag ]

def name_from_tags( _obj, *_tags, **kwargs ) :		
	# maybe this should remove any tags in taglist from _obj first?
	try : _replacelast = kwargs[ '_replacelast' ]
	except : _replacelast = True	

	try : name = _obj.name()
	except : name = _obj
	
	namesplit = [ name ]
	if _replacelast :		
		namesplit = name.rsplit( settings.name_string_delimeter, 1 )
	
	ret = namesplit[0]
	# ret = ''
	for tag in _tags :
		if tag : ret += settings.name_string_delimeter + get_tag( tag )
	
	# ret = settings.name_string_delimeter.join( set( ret.split( settings.name_string_delimeter ) ) )
	# r = ret.split( settings.name_string_delimeter )
	# r = list(set(r))
	# ret = settings.name_string_delimeter.join( r )
	# return namesplit[0] + ret
	return ret


#########################################################
# general
#########################################################


def make_groups_from_path_list( _pathlist, _topgroup=None, _stopbefore=0 ) :
	_ret = []
	lastgroup = pm.PyNode( _topgroup )
	
	for i, level in enumerate( _pathlist ) :

		if( i > len( _pathlist ) - abs( _stopbefore ) ) :
			break

		try : name = _pathlist[0].name
		except : name = level

		try : partname = level.PARTNAME
		except : partname = 'NULL'
		
		pm.select( None )
		groupname = '%s%s%s' % ( name, settings.name_string_delimeter, partname )
		groupname = name_from_tags( groupname, 'group', _replacelast=False )
				
		# check if the group exists and return the previosuly created group ifit does
		# otherwise create a new group
		group = None
		lastgroupchildren = lastgroup.getChildren()
		for child in lastgroupchildren :
			if( child.name().split( '|' )[-1] == groupname ) :
				group = child
				break		
		if( not group ) :
			group = pm.group( n=groupname )
			group.setParent( lastgroup )

		_ret.append( group )
		lastgroup = group

	pm.select( lastgroup )
	return _ret

def get_full_class_inheritance( _cls ) :
	bases = list( _cls.__bases__ )
	for base in bases :
		bases.extend( get_full_class_inheritance( base ) )
	return bases

def is_subclass( _obj, _class ) :
	isSubclass = False	
	bases = get_full_class_inheritance( _obj.__class__ )
	classname = _class.__name__
	for base in bases :
		basename = base.__name__
		if( basename.split( '.' )[-1] == classname ) :
			isSubclass = True
		# print base, _class
		# if( base == _class ) : isSubclass = True

	return isSubclass

#########################################################
# math
#########################################################


def aim_axis_to_vectors( _xyz ) :
	rotationorderdict = {
		'XYZ' : ( ( 1, 0, 0 ), ( 0, 1, 0 ) ),
		'YZX' : ( ( 0, 1, 0 ), ( 0, 0, 1 ) ),
		'ZXY' : ( ( 0, 0, 1 ), ( 1, 0, 0 ) ),
	}
	return rotationorderdict[ _xyz.upper() ]

def aim_axis_to_rotate_order( _xyz ) :
	i1, i2, i3 = _xyz
	return ''.join( ( i3, i1, i2 ) )

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

def distance_between( o1, o2 ) :
	try :
		o1pos = o1.getTranslation( space='world' )
		o2pos = o2.getTranslation( space='world' )
	except :
		err( 'Could not get translations of either %s or %s. Are they transforms?' % ( o1, o2 ) )
	return abs( o1pos.distanceTo( o2pos ) )

