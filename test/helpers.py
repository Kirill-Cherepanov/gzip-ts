import os
import gzip
import shutil
import subprocess as sp

"""
Convenience function for running a command bash-like

@param command- string version of a command to run on
@param shell- Whether to run this through the shell; used in subprocess.Popen (default: true)
@return Object with properties 'returncode', 'stdout', and 'stderr'
"""
def run_cmd(command, shell=True):
	process = sp.Popen(command, shell=shell, stdout = sp.PIPE, stderr = sp.PIPE)
	stdout, stderr = process.communicate()
	returncode = process.returncode
	return {'returncode' : returncode, 'stdout' : stdout, 'stderr' : stderr}

def read_gzip_file(filepath):
  with gzip.open(filepath, 'rt') as f:
    return f.read()

def diff_compressed(file1, file2):
  return read_gzip_file(file1) == read_gzip_file(file2)


def diff(file1, file2):
  with open(file1, 'r') as f1:
    content1 = f1.read()
  with open(file2, 'r') as f2:
    content2 = f2.read()
  return content1 == content2

def compress(input, output, level):
  with open(input, 'rb') as f_in:
    with open(output, 'wb') as f_out_file: 
      with gzip.GzipFile(fileobj=f_out_file, mode='wb', compresslevel=level, filename=os.path.basename(input)) as f_out:
        shutil.copyfileobj(f_in, f_out)
