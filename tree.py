"""

jointchain <--- bind chain
	rig
		subrig
			jointchain
			jointchain
			jointchain
		subrig	
			jointchain

"""


class TreeNode( object ) :
	def __init__( self, _parent=None, _value=None ) :
		self.__value = _value
		if not self.__value : self.__value = self		
		self.__parent = _parent
		self.__children = []

	def add_child( self, _value ) :
		child = TreeNode( self, _value )
		self.children.append( child )

	def tree_parent( self ) :
		return self.__parent

	def tree_children( self ) :
		return self.__children

	def tree_siblings( self ) :
		return self.parent().children()

