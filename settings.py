

debug = True
should_error = False

name_string_delimeter = '_'
attrname = 'th_autorig_nodecheck'

staticgroupsdict = {
	'geometry'		: 'GEOMETRY_GRP',
	'skeleton'		: 'SKELETON_GRP',
	'rig'			: 'RIG_GRP',
	'controls'		: 'CONTROLS_GRP',
}

tagdict = {
	None				: '',
	'fkRig'				: 'FKJ',
	'IkChainrig'		: 'IKJ',
	'BaseBlendrig'		: 'BJ',
	'control'			: 'CNTRL',	
	'IkHandle'			: 'HND',
	'IkEffector'		: 'EFF',
	'AnimCurveUL'		: 'ACUL',
	'MultiplyDivide'	: 'MULTDIV',
	'PlusMinusAverage'	: 'PMA',
	'sdk' 				: 'SDK',
	'zero' 				: 'ZERO',
	'ik' 				: 'IK',
	'ikdriver' 			: 'DRIVER',
	'fk' 				: 'FK',
	'polevector' 		: 'PV',
	'ikfkswitcher' 		: 'IKFK'
}