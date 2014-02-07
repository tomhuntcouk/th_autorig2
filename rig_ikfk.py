import pymel.all as pm

from rig_basic import BasicRig
import utils




class FkRig( BasicRig ) :
	def __init__( self ) :
		super( FkRig, self ).__init__()

	def create( self, _jointchain=None ) :
		super( FkRig, self ).create( _jointchain )

		

