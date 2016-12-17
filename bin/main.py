#!/usr/bin/env python3

import os
import subprocess
import sys
import json
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

with open('../conf/settings.json') as data_file:
    data = json.load(data_file)

number_of_projects = len(data['projects']['project'])

for project_index in range(number_of_projects):
    project_data = data['projects']['project'][project_index]
    project_name = project_data['name']
    project_home = project_data['project-home']
    deploy_dir = project_data['deploy-dir']
    git_url = project_data['git-url']
    isSync = project_data['sync']
    branch = project_data['branch']

    artifact_data = project_data['artifacts']['artifact']

    print('Pulling changes of project ' + project_name + ' ' + branch + ' branch')
    os.chdir(project_home)

    # subprocess.call(["git fetch --all"], shell=True)
    # os.system('git checkout ' + branch)

    for artifact_index in range(len(artifact_data)):
        artifact_name = artifact_data[artifact_index]['name']
        artifact_type = artifact_data[artifact_index]['type']
        pprint(artifact_data[artifact_index]['source-path'])
        artifact_source_path = artifact_data[artifact_index]['source-path']
        artifact_deploy_path = artifact_data[artifact_index]['deploy-path']

        path_to_artifact = os.path.join(project_home, artifact_source_path)
        os.chdir(path_to_artifact)

        # subprocess.call(["mvn clean install"], shell=True)

        if 'properties' in artifact_data[artifact_index]:
            property_data = artifact_data[artifact_index]['properties']

            for property_index in range(len(property_data['property'])):
                property_source_path = property_data['property'][property_index]['source-path']
                property_deploy_path = property_data['property'][property_index]['deploy-path']
                property_file_name = property_data['property'][property_index]['filename']

                property_source_full_path = os.path.join(project_home, artifact_source_path, property_source_path,
                                                         property_file_name)
                property_deploy_full_path = os.path.join(project_home, artifact_source_path, property_deploy_path,
                                                         property_file_name)
                source_file_contents = dict(line.strip().split('=') for line in open(property_source_full_path))
                deploy_file_contents = dict(line.strip().split('=') for line in open(property_deploy_full_path))
                #
                # for property_index in range(len(project_data)):
                #     print(artifact_data[artifact_index]['properties'])
                #     print('yyy')
# name = parsedXml.get('project_0').get('name')
# project_home = parsedXml.get('project_0').get('project-home')
# branch = parsedXml.get('project_0').get('branch')
# artifact = parsedXml.get('project_0').get('artifacts').get('artifact_0')
#
# print('Pulling changes of project ' + name + ' ' + branch + ' branch')
# os.chdir(project_home)
#
# subprocess.call(["git fetch --all"], shell=True)
# os.system('git checkout ' + branch)
#
# artifact_source_path = artifact.get('source-path')
# artifact_deploy_path = artifact.get('deploy-path')
# artifact_type = artifact.get('type')
# artifact_name = artifact.get('name')
# artifact_properties = artifact.get('properties')
#
# print('Building ' + artifact_name)
#
# os.chdir(artifact_source_path)
#
# H = dict(line.strip().split('=') for line in open(project_home + '/' + artifact_source_path))
#
# # subprocess.call(["mvn clean install"], shell=True)
#
# print(artifact)
