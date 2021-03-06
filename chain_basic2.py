import pymel.all as pm
import copy

from virtual import BaseVirtual
from skeleton2 import RigJoint

import settings, utils


class Jointchain( BaseVirtual, pm.Transform ) :
	PARTNAME = 'Jointchain'

	@classmethod
	def _preCreateVirtual( cls, **kwargs ) :
		kwargs, pkwargs = super( Jointchain, cls )._preCreateVirtual( **kwargs )
			
		# ensure we have start and end joints to get teh entire chain from and pass to post
		startJoint = kwargs.pop( 'startJoint' )
		endJoint = kwargs.pop( 'endJoint' )
		masterJointChain = kwargs.pop( 'masterJointChain' )
		if( not startJoint or not endJoint ) :
			utils.err( 'You need to specify startJoint and endJoint to create a Jointchain' )
			return False
		else :
			pkwargs = { 
				'startJoint' : startJoint,
				'endJoint' : endJoint,
				'masterJointChain' : masterJointChain
			}
			return kwargs, pkwargs

	@classmethod
	def _postCreateVirtual( cls, node, **kwargs ) :
		super( Jointchain, cls )._postCreateVirtual( node, **kwargs )
		self = pm.PyNode( node )

		# get the joints in the chain...
		jointlist = Jointchain.get_chain( kwargs['startJoint'], kwargs['endJoint'] )
		# ensure they're in a good state
		jointlist = cls.clean_jointlist( jointlist )
		# convert to rigjoints
		if( jointlist ) :
			rigjoints = []
			minorrigjoints = {}
			for joint in jointlist :
				if( RigJoint.convert( joint ) ) :
					rigjoint = pm.PyNode( joint )
					rigjoints.append( rigjoint )
					minorrigjoints[ rigjoint ] = []
		
		self.set( 'rigjoints', rigjoints )
		self.set( 'minorrigjoints', minorrigjoints )
		# if this is not a masterJointChain, we should tidy it's joints under it
		if( not kwargs[ 'masterJointChain' ] ) :
			self.get( 'rigjoints' )[0].setParent( self )


	def orient( self, orientchildless=True ) :
		for rigjoint in self.get( 'rigjoints' ) :
			rigjoint.orient( orientchildless )

	def split( self, jointid, numsplits ) :
		rigjoint = self.get( 'rigjoints' )[ jointid ]
		minorrigjoints = self.get( 'minorrigjoints' )
		minorrigjoints[ rigjoint ] = rigjoint.split( numsplits )
		self.set( 'minorrigjoints', minorrigjoints )

	def duplicate( self, *tags, **kwargs ) :
		# we will manually recreate the jointchain to ensure instance attributes are
		# properly created
		# we will duplicate each joint individually to ensure it is created correctly
		try : simple = kwargs[ 'simple' ]
		except : simple = False

		# first duplicate just the major rigjoints
		lastduplicaterigjoint = None
		for rigjoint in self.get('rigjoints' ) :
			# duplicate rigjoint with new name and parent to last joint
			duplicaterigjointname = utils.name_from_tags( rigjoint, *tags )
			duplicaterigjoint = rigjoint.duplicate( simple=True, name=duplicaterigjointname )
			duplicaterigjoint.setParent( lastduplicaterigjoint )
			lastduplicaterigjoint = duplicaterigjoint

			# now duplicate any minorjoints if needed
			if( not simple ) :
				duplicateminorrigjoints = {}
				for minorrigjoint in self.get( 'minorrigjoints' )[ rigjoint ] :
					









	@staticmethod
	def get_chain( startjoint, endjoint ) :
		if not Jointchain.check_jointchain( [ startjoint, endjoint ] ) :
			return False
		
		# get the joint chain
		alldescendants = startjoint.listRelatives( ad=True )[::-1]
		jointlist = [ startjoint ]
		for joint in alldescendants :
			jointlist.append( joint )
			if( joint == endjoint ) :
				break	
		return jointlist

	@staticmethod
	def clean_jointlist( jointlist ) :
		# make sure our list of joints is in order and in a good state to proceed
		if( not len( jointlist ) ) :
			utils.err( 'The jointlist submitted is empty.' )
			return False

		# sort by number of parents
		# as jointlist is only a list of joints they *could* be in any order		
		jointlist = Jointchain.sort_jointlist( jointlist )

		# check that all joints are in the same chain
		if( not Jointchain.check_jointchain( jointlist ) ) :
			return False

		return jointlist

	@staticmethod
	def check_jointchain( jointlist ) :
		if( not len( jointlist ) ) :
			utils.err( 'The jointlist submitted is empty.' )
			return False
		alldescendants = jointlist[0].listRelatives( ad=True )
		for joint in jointlist[1:] :
			if( joint not in alldescendants ) :
				utils.err( 'Joint %s not a descendant of %s. Stopping checks' % ( joint.name(), jointlist[0].name() ) )
				return False
		return True

	@staticmethod
	def sort_jointlist( jointlist ) :
		jointdict = {}
		for joint in jointlist :
			jointdict[ len( joint.getAllParents() ) ] = joint
		jointlist = [ v for i, v in sorted( jointdict.items() ) ]
		return jointlist



