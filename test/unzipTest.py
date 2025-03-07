import os
from colorama import Fore
from helpers import run_cmd, diff, compress

outDirDefault = 'test-outs'
testDirDefault = 'test-files'
gunzipPath = os.path.join('..', 'bin', 'gunzip.js')

"""
Run a single test

@param tFile- required; the file to check against (uncompressed data)
@param level- optional (default: all); the compression level [1-9]
@return True if all tests passed; False if at least one test failed
"""
def runTest(tFile, level=None, outDir=outDirDefault):
	passed = True

	if level == None:
		for x in range(1, 10):
			if runTest(tFile, x) == False:
				passed = False

		return passed

	out1 = os.path.join(outDir, '%(file)s.%(level)d.gz' % {'file': os.path.basename(tFile), 'level' : level})
	out2 = os.path.join(outDir, '%(file)s.%(level)d' % {'file' : os.path.basename(tFile), 'level' : level})

	compress(tFile, out1, level)
	run_cmd(f'node {gunzipPath} --file {out1} --output {out2}')

	if diff(tFile, out2):
		status = Fore.GREEN + 'PASSED' + Fore.RESET
	else:
		passed = False
		status = Fore.RED + 'FAILED' + Fore.RESET
	
	print('Level %(level)d: %(status)s' % {'level' : level, 'status' : status})

	return passed

"""
Runs all tests on the given level. This iterates throuth the testDir directory defined above.

@param level- The level to run on [1-9] (default: None, runs on all levels all)
@return True if all levels passed, False if at least one failed
"""
def runAll(level=None, testDir=testDirDefault, outDir=outDirDefault):
	passed = True
	for tFile in os.listdir(testDir):
		fullPath = os.path.join(testDir, tFile)

		print(Fore.YELLOW + tFile + Fore.RESET)

		if runTest(fullPath, level) == False:
			passed = False

		print('')
	
	return passed
