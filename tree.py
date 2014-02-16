import re

import utils

"""

jointchain <--- bind chain
	rig
		subrig
			jointchain
				control
				control
			jointchain
			jointchain
		subrig	
			jointchain

"""



class TreeNode( object ) :
	PARTNAME = 'treeNode'

	# def __unicode__( self ) :
	# 	if( self.__value == self ) :
	# 		return self
	# 	else :
	# 		return '-----' + self.__value

	# def __str__( self ) :
	# 	return unicode( self ).encode( 'utf-8' )

	def __init__( self, _parent=None, _value=None ) :
		self.__value = _value
		if not self.__value : self.__value = self
		self.__parent = _parent
		self.__children = []

	def add_child( self, _value ) :		
		# # if _value is a TreeNode, use it
		# # otherwise we'll create a new TreeNode with _value as __value
		# # this is in case we want to include other objects in the hieraarchy

		if( utils.is_subclass( _value, TreeNode ) ) :
			child = _value
		else :
			child = TreeNode( _value=_value )
		
		self.__check_tree_children()

		# child = _value
		child.__parent = self
		self.__children.append( child )

	def tree_value( self ) :
		# if( hasattr( self, '__value') ) :
		# 	print 'hasattr'
		try :return self.__value
		except : return self

	def tree_parent( self ) :
		return self.__parent

	def tree_children( self, _partname=None ) :		
		self.__check_tree_children()
		if not _partname :
			return self.__children
		else :
			return [ c for c in self.__children if re.match( _partname, c.PARTNAME ) ]

	def tree_siblings( self ) :
		return self.tree_parent().tree_children()

	def tree_root( self ) :
		target = self
		while target.tree_parent():
			target = target.tree_parent()
		return target
	
	def tree_all_descendants( self, _ret=[] ) :
		for child in self.tree_children() :
			_ret.append( child )
			try :
				child.tree_all_descendants( _ret )
			except :
				pass
		return _ret

	def tree_all_parents( self ) :
		ret = []
		target = self
		while target.tree_parent() :
			ret.append( target )
			target = target.tree_parent()
		ret.append( target )
		return ret[::-1]

	def __check_tree_children( self ) :
		try :
			self.__children
			return True
		except :
			self.__children = []
			return False








