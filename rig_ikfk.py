import pymel.all as pm

from rig_basic import BasicRig
import controls
import utils




class FkRig( BasicRig ) :
	PARTNAME = 'fkRig'

	def __init__( self ) :
		super( FkRig, self ).__init__()

	def create( self, _jointchain=None ) :
		super( FkRig, self ).create( _jointchain )

		lastcontrol = None
		print self.tree_children()
		for rigjoint in self.tree_children( 'jointchain' )[0].rigjoints :
			control = controls.RigControl( n=rigjoint.name() )
			control.position_to_object( rigjoint )
			pm.orientConstraint( control, rigjoint )
			if( lastcontrol ) :
				pm.parentConstraint( lastcontrol, control, mo=True )
			zerogroup = control.zero_group()
			# if( zerogroup ) :
			# 	zerogroup.setParent( lastcontrol )
			lastcontrol = control
			self.add_child( control )

