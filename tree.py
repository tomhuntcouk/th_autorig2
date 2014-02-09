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

	def __init__( self, _parent=None, _value=None ) :
		self.__value = _value
		if not self.__value : self.__value = self		
		self.__parent = _parent
		self.__children = []

	def add_child( self, _value ) :		
		# # if _value is a TreeNode, use it
		# # otherwise we'll create a new TreeNode with _value as __value
		# # this is in case we want to include other objects in the hieraarchy

		# isTreeNode = False
		# for base in _value.__class__.__bases__ :
		# 	if( base.__name__ == 'TreeNode' ) :
		# 		isTreeNode = True
		# 		break

		# if( isTreeNode ) :
		# 	child = _value
		# else :
		# 	child = TreeNode( _value=_value )

		child = _value
		child.__parent = self
		# print '-', child, child.__parent
		self.__children.append( child )

	def tree_value( self ) :
		return self.__value

	def tree_parent( self ) :
		# print '=', self.__parent
		return self.__parent

	def tree_children( self, _partname=None ) :
		if not _partname :
			return self.__children
		else :
			return [ c for c in self.__children if c.PARTNAME == _partname ]

	def tree_siblings( self ) :
		return self.parent().children()

	def tree_root( self ) :		
		target = self
		c = 0
		while target.tree_parent() and c < 5:
			target = target.tree_parent()
		return target
		







