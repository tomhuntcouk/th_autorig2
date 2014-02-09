import pymel.all as pm

import copy

from tree import TreeNode
# from skeleton import RigJoint leads to:
# TypeError: Determined type is Joint, which is not a subclass of desired type RigJoint # 
# so we'll just:
import skeleton
# i think this is because we need to register the virtual class in every module
import utils, settings


class Jointchain( TreeNode ) :
	PARTNAME = 'jointchain'

	def __init__( self, _jointlist ) :
		super( Jointchain, self ).__init__()

		# partname will stay the same throughout the whole tree
		# we could therefore use self.root() to get the partname
		# self.partname = _partname
		self.copymother = None
		self.duplicates = []
		self.rigjoints = []
		self.minorrigjoints = {}

		clean_joints = Jointchain.clean_jointlist( _jointlist )
		if clean_joints : self.create_rigjoints( clean_joints )

	@classmethod
	def from_startend( cls, _startjoint, _endjoint ) :
		return cls( Jointchain.get_chain( _startjoint, _endjoint ) )

	def create_rigjoints( self, _jointlist ) :
		ret = []
		for joint in _jointlist :				
			if( skeleton.RigJoint.convert_to_virtual( joint ) ) :
				rigjoint = pm.PyNode( joint )
				self.rigjoints.append( rigjoint )
				self.minorrigjoints[ rigjoint ] = []
				ret.append( rigjoint )
 		return ret

 	def orient_jointchain( self, _orientchildless=True ) :
 		for rigjoint in self.rigjoints :
 			rigjoint.orient( _orientchildless )

 	def split_rigjoint( self, _pos, _numsplits ) :
 		rigjoint = self.rigjoints[ _pos ]
 		self.minorrigjoints[ rigjoint ] = rigjoint.split( _numsplits )

 	def duplicate_jointchain( self, _class=None, _tag=None, _simple=False ) :
 		# make a deep copy of self
		# loop through bones and replace rigjoint with a new one
		# loop through minorbones and replace minorbone with bone.duplicate	

		# we could duplicate the top joint and then compare with original to find the minorjoints
		# creating each joint individually seems to be more direct though

		dupjointchain = copy.deepcopy( self )
		dupjointchain.copymother = self
		lastrigjoint = None
		pm.select( None )
		for i, rigjoint in enumerate( dupjointchain.rigjoints ) :
			duprigjointname = utils.name_from_tags( rigjoint, _class, _tag )
			duprigjoint = rigjoint.duplicate( n=duprigjointname )[0]
			dupjointchain.rigjoints[i] = duprigjoint
			duprigjoint.setParent( lastrigjoint )
			lastrigjoint = duprigjoint

			# _simple copies only major rigjoints
			if( not _simple ) :
				dupjointchain.minorrigjoints[ duprigjoint ] = []
				# duplicate each minorrigjoint, add it to it's duplicated major rigjoint array of minor rigjoints				
				for minorrigjoint in dupjointchain.minorrigjoints[ rigjoint ] :
					dupminorrigjointname = utils.name_from_tags( minorrigjoint, _class, _tag )
					dupminorrigjoint = minorrigjoint.duplicate( n=dupminorrigjointname )[0]
					dupjointchain.minorrigjoints[ duprigjoint ].append( dupminorrigjoint)
					dupminorrigjoint.setParent( lastrigjoint )
					lastrigjoint = dupminorrigjoint
				# delete the original rigjoint entry in the dict
				del dupjointchain.minorrigjoints[ rigjoint ]
				
		self.duplicates.append( dupjointchain )
		return dupjointchain


	############################################################


	@staticmethod
	def clean_jointlist( _jointlist ) :
		if( not len( _jointlist ) ) :
			utils.err( 'The jointlist submitted is empty.' )
			return False

		# sort by number of parents
		# as _jointlist is only a list of joints they *could* be in any order		
		_jointlist = Jointchain.sort_jointlist( _jointlist )

		# check that all joints are in the same chain
		if( not Jointchain.check_jointchain( _jointlist ) ) :
			return False

		return _jointlist

	@staticmethod
	def sort_jointlist( _jointlist ) :
		jointdict = {}
		for joint in _jointlist :
			jointdict[ len( joint.getAllParents() ) ] = joint
		_jointlist = [ v for i, v in sorted( jointdict.items() ) ]
		return _jointlist

	@staticmethod
	def check_jointchain( _jointlist ) :
		if( not len( _jointlist ) ) :
			utils.err( 'The jointlist submitted is empty.' )
			return False
		alldescendants = _jointlist[0].listRelatives( ad=True )
		for joint in _jointlist[1:] :
			if( joint not in alldescendants ) :
				utils.err( 'Joint %s not a descendant of %s. Stopping checks' % ( joint.name(), _jointlist[0].name() ) )
				return False
		return True

	@staticmethod
	def get_chain( _startjoint, _endjoint ) :
		if not Jointchain.check_jointchain( [ _startjoint, _endjoint ] ) :
			return False
		
		# get the joint chain
		alldescendants = _startjoint.listRelatives( ad=True )[::-1]
		jointlist = [ _startjoint ]
		for joint in alldescendants :
			jointlist.append( joint )
			if( joint == _endjoint ) :
				break	
		return jointlist


