import pymel.all as pm

from virtual import RigTransform

pm.factories.registerVirtualClass( RigTransform, nameRequired=False )

def main() :

	RigTransform( n='test' )
	# virtual.RigTransform( n='test' )
