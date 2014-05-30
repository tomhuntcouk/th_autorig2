import pymel.all as pm

try :
	from collections import OrderedDict
except ImportError :
	from ordereddict import OrderedDict

from virtual import BaseVirtual





class BaseRig( BaseVirtual, pm.Transform ) :
	PARTNAME = 'BaseRig'



class BindRig( BaseRig ) :
	PARTNAME = 'BindRig'
	

	@classmethod
	def _postCreateVirtual( cls, node, **kwargs ) :
		super( BindRig, cls )._postCreateVirtual( node, **kwargs )
		node = pm.PyNode( node )
		node.set( 'masterjointchain', '' )


	def create( self, divisionstuple=( 0, 0 ) ) :
		jointchain = self.children( rigtype='Jointchain' )[0]
		self.set( 'masterjointchain', jointchain )
		self.get( 'masterjointchain' ).PARTNAME = 'masterjointchain'
		
		# ready masterjointchain for having subrigs created from it
		self.get( 'masterjointchain' ).orient()
		for i, numdivisions in enumerate( divisionstuple ) :
			self.get( 'masterjointchain' ).split( i, numdivisions )


class BasicRig( BaseRig ) :

	def create( self, jointchain=None ) :
		# get masterjointchain and copy it if no _jointchain is specified
		if( not jointchain ) :
			jointchain = self.root().get( 'masterjointchain' ).duplicate( self.PARTNAME )
		# self.add_child( jointchain )
		# pm.select( jointchain )
			