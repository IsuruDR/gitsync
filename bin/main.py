#!/usr/bin/env python3

import os
import subprocess
import sys
import json
from pprint import pprint
import logging

logging.basicConfig(filename='../logs/info.log', level=logging.DEBUG)

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
        artifact_final_name = artifact_data[artifact_index]['final-name']
        artifact_version = ''
        if 'version' in artifact_data[artifact_index]:
            artifact_version = artifact_data[artifact_index]['version']

        if 'properties' in artifact_data[artifact_index]:
            property_data = artifact_data[artifact_index]['properties']

            for property_index in range(len(property_data['property'])):
                property_source_path = property_data['property'][property_index]['source-path']
                property_deploy_path = property_data['property'][property_index]['deploy-path']
                property_file_name = property_data['property'][property_index]['filename']

                property_source_full_path = os.path.join(project_home, artifact_source_path, property_source_path,
                                                         property_file_name)
                if type == 'jar':
                    property_deploy_full_path = property_deploy_path
                else:
                    property_deploy_full_path = os.path.join(deploy_dir, artifact_deploy_path, property_deploy_path,
                                                             property_file_name)

                source_file_contents = dict(line.strip().split('=', 1) for line in open(property_source_full_path))
                deploy_file_contents = dict(line.strip().split('=', 1) for line in open(property_deploy_full_path))

                updated_properties = ''
                is_keys_updated = False
                for key in source_file_contents:
                    if key in deploy_file_contents:
                        updated_properties = updated_properties + key + ' = ' + deploy_file_contents[key] + '\n'
                    else:
                        is_keys_updated = True
                        updated_properties = updated_properties + key + ' = ' + source_file_contents[key] + '\n'
                        logging.info(' (+) ' + key + ' = ' + source_file_contents[key] + ' => ' + property_file_name)

                property_file = open(property_source_full_path, 'w')
                property_file.write(updated_properties)
                property_file.close()

        path_to_artifact = os.path.join(project_home, artifact_source_path)
        os.chdir(path_to_artifact)

        subprocess.call(["mvn clean install"], shell=True)

        artifact_deploy_full_path = os.path.join(deploy_dir, artifact_deploy_path)
        print('Copying ' + artifact_final_name + '-' + artifact_version + ' to ' + artifact_deploy_full_path)

        if artifact_version is None or artifact_version == '':
            os.system('cp ' + os.path.join('target', artifact_final_name + '.' + artifact_type)
                      + ' ' + artifact_deploy_full_path)
        else:
            os.system('cp ' + os.path.join('target', artifact_final_name + '-' + artifact_version + '.' + artifact_type)
                      + ' ' + artifact_deploy_full_path)

