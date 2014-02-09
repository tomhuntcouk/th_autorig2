import pymel.all as pm

try :
	from collections import OrderedDict
except ImportError :
	from ordereddict import OrderedDict

from tree import TreeNode
from chain_basic import Jointchain


tidydict = {
	'jointchain' 	: settings.staticgroupsdict[ 'rig' ],
	'rigControl'	: settings.staticgroupsdict[ 'controls' ],
}


class BindRig( TreeNode ) :
	PARTNAME = 'bindRig'
	
	def __init__( self, _name  ) :
		super( BindRig, self ).__init__()

		self.name = _name		
		self.masterjointchain = None
		# self.add_child( _jointchain )
	
	def create( self, _jointchain, _divisionstuple ) :		
		# keeping these two references to _jointchain feels weird
		self.add_child( _jointchain )
		self.masterjointchain = _jointchain 

		# ready masterjointchain for having subrigs created from it
		self.masterjointchain.orient_jointchain()
		for i, numdivisions in enumerate( _divisionstuple ) :
			self.masterjointchain.split_rigjoint( i, numdivisions )


class BasicRig( TreeNode ) :
	PARTNAME = 'basicRig'
	
	def __init__( self ) :
		super( BasicRig, self ).__init__()

	def create( self, _jointchain=None ) :
		# get masterjointchain and copy it if no _jointchain is specified
		if( not _jointchain ) :
			self.add_child( self.tree_root().masterjointchain.duplicate_jointchain( self.PARTNAME ) )
		else :
			self.add_child( _jointchain )

	def tidy( self ) :
		alldescendants = self.tree_all_descendants()
		for descendant in alldescendants :
			group = tidydict[ descendant.PARTNAME ]







