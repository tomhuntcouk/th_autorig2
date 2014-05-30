import pymel.all as pm

from virtual import BaseVirtual

import utils, settings



class RigJoint( BaseVirtual, pm.Joint ) :
	PARTNAME = 'RigJoint'

	

