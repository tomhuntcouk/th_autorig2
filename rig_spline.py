import pymel.all as pm

from tree import TreeNode
# from chain_basic import Jointchain

from rig_basic import *
import controls
import utils, settings


class SplineRig( BasicRig ) :
	PARTNAME = 'splineRig'

	def create( self, _jointchain=None ) :
		super( SplineRig, self ).create( _jointchain )

