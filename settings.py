

debug = True
should_error = False

name_string_delimeter = '_'
attrname = 'nodecheck'

rotationorder = 'XYZ'

staticgroupsdict = {
	'geometry'		: 'GEOMETRY_GRP',
	'skeleton'		: 'SKELETON_GRP',
	'rig'			: 'RIG_GRP',
	'controls'		: 'CONTROLS_GRP',
}

staticcontrols = {
	'ikfkblend'		: 'ikfkBlend',
}

tagdict = {
	None				: '',
	# autorig types
	'FkRig'				: 'FKJ',
	'IkRig'				: 'IKJ',
	'Spline'			: 'S',
	'BlendRig'			: 'BJ',
	'BaseRig'			: 'BJ',
	'SplineRig'			: 'SIKJ',
	'Control'			: 'CNTRL',	

	# maya types
	'ikhandle'			: 'HND',
	'ikeffector'		: 'EFF',
	'animcurveUL'		: 'ACUL',
	'multiplydivide'	: 'MULTDIV',
	'plusminusaverage'	: 'PMA',
	'sdk' 				: 'SDK',
	'zero' 				: 'ZERO',
	'ik' 				: 'IK',
	'driver' 			: 'DRIVER',
	'fk' 				: 'FK',
	'polevector' 		: 'PV',
	'ikfkswitcher' 		: 'IKFK',
	'group'				: 'GRP',
	'curve'				: 'CRV',
	'nurbs'				: 'NRB',
	'cluster'			: 'CLS',
	'follicle'			: 'FOL',
	
	# other
	'blend'				: 'BLEND',
	'squashstretch'		: 'SQUSTR',
	'rotateaddin'		: 'RADDIN',
	'transformaddin'	: 'TADDIN',
	'scaleaddin'		: 'SADDIN',
	'start'				: 'START',
	'mid'				: 'MIDDLE',
	'end'				: 'END',
}
