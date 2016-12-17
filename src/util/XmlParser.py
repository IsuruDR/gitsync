#!/usr/bin/env python3

import xml.etree.ElementTree as ET


class XmlParser:
    @staticmethod
    def parse_xml(file_path):
        projects = ET.parse(file_path)

        projects_map = {}

        project_index = 0
        for project in projects.iter('project'):

            project_details = {}

            name = ET.Element(project.find('name'))
            git_url = ET.Element(project.find('git-url'))
            is_sync = ET.Element(project.find('sync'))
            branch = ET.Element(project.find('branch'))
            source_dir = ET.Element(project.find('project-home'))
            deploy_dir = ET.Element(project.find('deploy-dir'))
            artifacts = ET.ElementTree(project.find('artifacts'))

            artifacts_map = {}

            artifact_index = 0
            for artifact in artifacts.iter('artifact'):

                artifact = ET.ElementTree(artifact)
                properties = artifact.find('properties')

                property_details = {}

                property_configs = {}
                if properties is not None:
                    property_index = 0
                    for property_value in properties:
                        property_value = ET.ElementTree(property_value)

                        property_details['filename'] = property_value.find('filename').text
                        property_details['source-path'] = property_value.find('source-path').text
                        property_details['deploy-path'] = property_value.find('deploy-path').text
                        property_configs['property_' + repr(property_index)] = property_details
                        property_index += 1
                        print(property_configs)

                artifact_details = {'name': artifact.find('name').text,
                                    'type': artifact.find('type').text,
                                    'source-path': artifact.find('source-path').text,
                                    'deploy-path': artifact.find('deploy-path').text,
                                    'properties': property_configs}
                artifacts_map['artifact_' + repr(artifact_index)] = artifact_details
                artifact_index += 1

            project_details['name'] = name.tag.text
            project_details['git-url'] = git_url.tag.text
            project_details['sync'] = is_sync.tag.text
            project_details['branch'] = branch.tag.text
            project_details['project-home'] = source_dir.tag.text
            project_details['deploy-dir'] = deploy_dir.tag.text
            project_details['artifacts'] = artifacts_map

            projects_map['project_' + repr(project_index)] = project_details
            project_index += 1
        projects_map['number-of-projects'] = project_index
        return projects_map
