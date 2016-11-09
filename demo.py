import subprocess

#This script demonstrates:
# 1. how to call a shell script within Python,
# 2. how to retrieve the returned information.


commands =[
	'searchvariantsets',
	'getvariantset 123',
	'searchvariants 123 abc 100 200 csi01 csi02 csi05 csi100 ',
	'getvariant 123',
	'searchcallsets 123 xyz B_789',
	'getcallset 123',
	'searchbiosamples B_789',
	'getbiosample B_789'
]
for cmd in commands:
	p = subprocess.Popen('python3 dataAPI.py %s' %cmd, shell=True, stdout=subprocess.PIPE, universal_newlines = True)
	print('Result of %s :' %cmd)

	#communicate() will return both the running result and the return code.
	#rstrip() is to remove the extra newline
	print( p.communicate()[0].rstrip() )
	print()
	retval =p.wait()
