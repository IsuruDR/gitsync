#!/usr/bin/env python3

import os
import shlex
import subprocess
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.util.XmlParser import XmlParser
from src.util.Spinner import Spinner


parsedXml = XmlParser.parse_xml('../conf/settings.xml')

name = parsedXml.get('project_0').get('name')
source_dir = parsedXml.get('project_0').get('project-home')
branch = parsedXml.get('project_0').get('branch')
artifact = parsedXml.get('project_0').get('artifacts').get('artifact_0')

print('Pulling changes of project ' + name + ' ' + branch + ' branch')
os.chdir(source_dir)
git_cmd = 'git pull'
kwargs = {}
kwargs['stdout'] = subprocess.PIPE
kwargs['stderr'] = subprocess.PIPE
proc = subprocess.Popen(shlex.split(git_cmd), **kwargs)

Spinner.load_spinner()

(stdout_str, stderr_str) = proc.communicate()
return_code = proc.wait()
print(return_code)
print(stdout_str)

if return_code == 0:
    os.system('git checkout ' + branch)

    artifact_source_path = artifact.get('source-path')
    artifact_deploy_path = artifact.get('deploy-path')
    artifact_type = artifact.get('type')
    artifact_name = artifact.get('name')

    os.chdir(artifact_source_path)
    os.system('mvn clean install')

    print(artifact)
else:
    print('Error occurred while pulling changes')
