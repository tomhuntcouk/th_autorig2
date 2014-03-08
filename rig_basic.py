import pymel.all as pm

try :
	from collections import OrderedDict
except ImportError :
	from ordereddict import OrderedDict

from tree import TreeNode
# from chain_basic import Jointchain

import settings, utils

tidydict = {
	'treeNode' 			: ( settings.staticgroupsdict[ 'rig' ], 		'.tree_value()' 	),
	'masterjointchain' 	: ( settings.staticgroupsdict[ 'skeleton' ], 	'.rigjoints[0]' 	),
	'jointchain' 		: ( settings.staticgroupsdict[ 'rig' ], 		'.rigjoints[0]' 	),
	'rigControl'		: ( settings.staticgroupsdict[ 'controls' ], 	'.zero_group()' 	),
}


class BaseRig( TreeNode ) :
	PARTNAME = 'bindRig'

	# def __init__( self ) :
	# 	super( BaseRig, self ).__init__()
	# 	self.mainjointchain = None


	def tidy( self ) :

		# we will need to fully parent the bind joints together
		# at some point
		# perhaps this should be handled by BindRig?

		allrigs = self.tree_children( '.*Rig' )
		allother = list( set( self.tree_children() ) - set( allrigs ) )
		
		for rig in allrigs :
			rig.tidy()

		for child in allother :
			# create the group hierarchy to the required level and parent to it
			# we'll use tidydict to specify which object to parent

			try : partname = child.tree_value().PARTNAME
			except : partname = 'treeNode'
			if( not partname in tidydict.keys() )  :
				partname = 'treeNode'

			topgroup = tidydict[ partname ][0]
			obj = eval( 'child' + tidydict[ partname ][1] )

			pathlist = child.tree_all_parents()
			# we'll stop creating groups just before the last level
			# this makes the last group at the rig level, rather than component level
			groups = utils.make_groups_from_path_list( pathlist, topgroup, -2 )
			group = groups[-1]

			try :
				if( obj.getParent() != group ) :					
					obj.setParent( group )
			except RuntimeError, e :
				utils.err( e.message )
			except AttributeError, e :
				utils.err( e.message )
				pass



class BindRig( BaseRig ) :
	PARTNAME = 'bindRig'
	
	def __init__( self, _name  ) :
		super( BindRig, self ).__init__()
		self.name = _name		
		self.masterjointchain = None
	
	def create( self, _jointchain, _divisionstuple=( 0, 0 ) ) :		
		# keeping these two references to _jointchain feels weird
		self.masterjointchain = _jointchain 
		self.masterjointchain.PARTNAME = 'masterjointchain'
		self.add_child( _jointchain )

		# ready masterjointchain for having subrigs created from it
		self.masterjointchain.orient_jointchain()
		for i, numdivisions in enumerate( _divisionstuple ) :
			self.masterjointchain.split_rigjoint( i, numdivisions )



class BasicRig( BaseRig ) :
	PARTNAME = 'basicRig'
	
	def __init__( self ) :
		super( BasicRig, self ).__init__()
		# self.controls = OrderedDict()

	def create( self, _jointchain=None ) :
		# get masterjointchain and copy it if no _jointchain is specified
		if( not _jointchain ) :
			self.add_child( self.tree_root().masterjointchain.duplicate_jointchain( self.PARTNAME ) )
		else :
			self.add_child( _jointchain )



class BlendRig( BaseRig ) :
	PARTNAME = 'blendRig'

	def __init__( self ) :
		super( BlendRig, self ).__init__()
		self.blendattr = None

	def create( self, _jointchain=None ) :
		# get masterjointchain and copy it if no _jointchain is specified
		# this will be the blend chain
		if( not _jointchain ) :
			self.add_child( self.tree_root().masterjointchain.duplicate_jointchain( self.PARTNAME ) )
		else :
			self.add_child( _jointchain )
		
	def connect_rigs( self, _blendcontrol=None ) :

		# get the object the blend attr should be added to
		blendcontrol = _blendcontrol
		if( not blendcontrol ) :
			blendcontrolname = utils.name_from_tags( settings.staticcontrols[ 'ikfkblend' ], 'control' )
			blendcontrol = pm.PyNode( blendcontrolname )

		try :
			# create the blend attr
			blendattrname = utils.name_from_tags( self.tree_root().name, 'blend' )
			self.blendattr = utils.add_set_attr( blendcontrol, blendattrname, 0.0 )
		except :
			utils.err( 'Could not create blend attribute on %s' % ( blendcontrol ) )
			return False

		# blend between rigs onto blendjointchain

		jointchains = self.tree_children( 'jointchain' )
		if( len( jointchains ) != 1 ) :
			utils.err( '%s does not have ONE jointchain in it\'s children. Not sure which to use as the blend chain.' % ( self ) )
			return False
		blendjoints = jointchains[0].all_joints()
		rigs = self.tree_children( '.*Rig' )
		multdivdict = {}

		# set min/max values for blendattr
		self.blendattr.setMin( 0 )
		self.blendattr.setMax( len( self.tree_children( '.*Rig' ) ) - 1 )

		for i, rig in enumerate( rigs ) :	
			for jointchain in rig.tree_children( 'jointchain' ) :
				rigjoints = jointchain.all_joints()
				if( len( rigjoints ) != len( blendjoints ) ) :
					utils.wrn( '%s has a different number of joints to %s. Skipping...' % ( jointchain, jointchains[0] ) )
					continue

				# create a triangle curve with float time offset by j
				# by overlapping each triangle, n number of rigs can be blended
				# _/\____     
				# __/\___   this is how 3 rigs would blend together
				# ___/\__

				animcurve = pm.nodetypes.AnimCurveUL()
				animcurve.rename( utils.name_from_tags( self.tree_root().name, 'blend', rig.PARTNAME, 'animcurveUL' ) )

				offset = i
				pm.setKeyframe( animcurve, f=-1 + offset, v=0 )
				pm.setKeyframe( animcurve, f=0 	+ offset, v=1 )
				pm.setKeyframe( animcurve, f=1 	+ offset, v=0 )
				
				self.blendattr >> animcurve.input

				multdivdict[ rig ] = []

				for rigjoint in rigjoints :
					# vary input of joints rotation by animcurve output
					multdiv = pm.nodetypes.MultiplyDivide()
					multdiv.rename( utils.name_from_tags( rigjoint, 'blend', rig.PARTNAME, 'multiplydivide' ) )
					multdivdict[ rig ].append( multdiv )
					# connect animcurev and rotate to multdiv
					animcurve.output 	>> multdiv.input1X
					animcurve.output 	>> multdiv.input1Y
					animcurve.output 	>> multdiv.input1Z
					rigjoint.rotate		>> multdiv.input2

				for j, blendjoint in enumerate( blendjoints ) :
					# use a PMA node to blend between the rigs
					pma = pm.nodetypes.PlusMinusAverage()
					pma.rename( utils.name_from_tags( blendjoint, 'blend', rig.PARTNAME, 'plusminusaverage' ) )
					pma.operation.set( 1 )

					# connect everything up
					k = 0
					for rig, multdivlist in multdivdict.iteritems() :
						multdivlist[j].output >> pma.input3D[k]
						k += 1

					pma.output3D >> blendjoint.rotate

