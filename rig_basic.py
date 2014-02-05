import pymel.all as pm

try :
	from collections import OrderedDict
except ImportError :
	from ordereddict import OrderedDict

from tree import TreeNode
from chain_basic import Jointchain


# class BaseRig( TreeNode ) :
# 	PARTNAME = 'base'

# 	def __init__( self, _jointchain ) :
# 		super( BindRig, self ).__init__()

# 	def add_rig( self, _rig ) :
# 		self.add_child( _rig )


class BindRig( TreeNode ) :
	PARTNAME = 'bindRig'
	
	def __init__( self, _jointchain ) :
		super( BindRig, self ).__init__()

		self.add_child( _jointchain )
		





class BasicRig( TreeNode ) :
	PARTNAME = 'basicRig'
	
	def __init__( self, _jointchain ) :
		super( BasicRig, self ).__init__()
		self.partname = 'basicRig'

		# self.add_child( _jointchain )



