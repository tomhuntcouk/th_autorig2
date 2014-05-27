import pymel.all as pm
import pymel.core.nodetypes as pn

from rig_basic import *
import controls
import utils, settings


class FkRig( BasicRig ) :
	PARTNAME = 'fkRig'

	# def __init__( self ) :
	# 	super( FkRig, self ).__init__()

	def create( self, _jointchain=None ) :
		super( FkRig, self ).create( _jointchain )
		
		return True

	def addinSquashStretch( self ) :
		pass

	def addinDistributedTwist( self ) :
		pass



class IkRig( BasicRig ) :
	PARTNAME = 'ikRig'

	def create( self, _jointchain=None ) :
		super( IkRig, self ).create( _jointchain )

		jointchains = self.tree_children( 'jointchain' )
		if( len( jointchains ) != 1 ) :
			utils.err( 'IkRig children includes more than ONE jointchain. Not sure which to use. Skipping...' )
			return False		

		# create a simple joint chain
		simplejointchain = jointchains[0].duplicate_jointchain( self.PARTNAME, 'driver', _simple=True )
		self.add_child( simplejointchain )

		# create a curve between each pair of simple rigjoints
		# rebuild with numspan 2 and 3 degree
		# move vtx[1] and vtx[-2] to respective ends of curve
		# cluster start, mid and end of curve
		# parent clusters to respective rigjoints
		# group then point/parent constrain middle cluster to end clusters
		# for each minorjoint
		# 	closestpointoncurve node - get closest UV
		# 	curveInfoNode - get world pos of closest UV
		# 	worldposUV >> minorjoint.pos
		# some kind of normal constraint to create twist


		return True
		


	def addinSquashStretch( self ) :
		pass

	def addinDistributedTwist( self ) :
		pass
		

class IkFkBlendRig( BlendRig ) :
	PARTNAME = 'ikfkBlendRig'

	def __init__( self ) :
		pass

	def create( self, _jointchain=None ) :
		pass

		