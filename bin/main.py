import os
import subprocess, shlex
from classes.com.gitsync.util.XmlParser import XmlParser

parsedXml = XmlParser.parse_xml('../conf/settings.xml')

name = parsedXml.get('project_0').get('name')
source_dir = parsedXml.get('project_0').get('source-dir')
branch = parsedXml.get('project_0').get('branch')

print('Syncing with project ' + repr(name) + 's ' + repr(branch) + ' branch')
os.chdir(source_dir)
git_cmd = 'git pull origin ' + repr(branch)
kwargs = {}
kwargs['stdout'] = subprocess.PIPE
kwargs['stderr'] = subprocess.PIPE
proc = subprocess.Popen(shlex.split(git_cmd), **kwargs)
(stdout_str, stderr_str) = proc.communicate()
return_code = proc.wait()
print(return_code)
print(stdout_str)
