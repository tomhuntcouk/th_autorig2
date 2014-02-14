import pymel.all as pm

# try :
# 	from collections import OrderedDict
# except ImportError :
# 	from ordereddict import OrderedDict

from tree import TreeNode
# from chain_basic import Jointchain

import settings, utils

tidydict = {
	'jointchain' 	: ( settings.staticgroupsdict[ 'rig' ], 		'.rigjoints[0]' 	),
	'rigControl'	: ( settings.staticgroupsdict[ 'controls' ], 	'.zero_group()' 	),
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

	def tidy( self ) :
		pass


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
			# create the group hierarchy to the required level and parent to it
			# we'll use __tidydict to specify which object to parent
			topgroup = tidydict[ descendant.PARTNAME ][0]
			obj = eval( 'descendant' + tidydict[ descendant.PARTNAME ][1] )

			pathlist = descendant.tree_path_list()
			groups = utils.make_groups_from_path_list( pathlist, topgroup )
			group = groups[-1]

			obj.setParent( group )

class BlendRig( TreeNode ) :
	PARTNAME = 'blendRig'

	def __init__( self ) :
		super( BlendRig, self ).__init__()

	def create( self, _jointchain=None ) :
		# get masterjointchain and copy it if no _jointchain is specified
		# this will be the blend chain
		if( not _jointchain ) :
			self.add_child( self.tree_root().masterjointchain.duplicate_jointchain( self.PARTNAME ) )
		else :
			self.add_child( _jointchain )

		# create the blend attr
		blendcontrol = pm.PyNode( settings.staticcontrols[ 'ikfkblend' ] )
		self.ikfkblendattr = utils.add_set_attr( blendcontrol, 'ikfkblend', 0.0 )
		# initialize the min/max values
		self.ikfkblendattr.setMin( 0 )
		self.ikfkblendattr.setMax( len( self.tree_children( '*Rig' ) ) )

		
		















