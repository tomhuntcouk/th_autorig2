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


	def create( self, jointchain, divisionstuple=(0,0) ) :
		self.set( 'masterjointchain', jointchain )
		self.get( 'masterjointchain' ).PARTNAME = 'masterjointchain'
	
		self.get( 'masterjointchain' ).duplicate_chain()