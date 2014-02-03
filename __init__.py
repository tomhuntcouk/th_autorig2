import os

for mod in os.listdir( os.path.dirname( __file__ ) ) :
	if mod == '__init__.py' or mod[-3:] != '.py' :
		continue	
	m = __import__( mod[:-3], locals(), globals() )
	# print m
	reload( m )
del mod
