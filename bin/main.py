import sys
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

projects = ET.parse('settings.xml')

data_dict = defaultdict(list)

project = projects.find('project')
name = ET.Element(project.find('name'))
git_url = ET.Element(project.find('git-url'))
is_sync = ET.Element(project.find('sync'))
branch = ET.Element(project.find('sync'))
source_dir = ET.Element(project.find('source-dir'))
deploy_dir = ET.Element(project.find('deploy-dir'))
artifacts = ET.ElementTree(project.find('artifacts'))
available_artifacts = artifacts.findall('artifact')

for artifact in available_artifacts:
    artifact = ET.ElementTree(artifact)
    properties = artifact.find('properties')

    property_details = {}

    for property_value in properties:
        property_value = ET.ElementTree(property_value)

        property_details['filename'] = property_value.find('filename').text
        property_details['path'] = property_value.find('path').text

    artifact_details = {'name': artifact.find('name').text,
                        'type': artifact.find('type').text,
                        'source-path': artifact.find('source-path').text,
                        'deploy-path': artifact.find('deploy-path').text,
                        'properties': property_details}
    print(artifact_details)

print(name.tag.text)
# print(root[0][6][0])
# for child in root:
#     print(child.tag)
#     xml[root.tag] = child.tag

# print(xml)
