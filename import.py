import csv
import os
from sys import argv

import utils
from fields import reconcile_fields

# args should be Repo URL and CSV file
github_repo_url = argv[1]
csv_file = argv[2]
filepath = os.path.join(os.getcwd(), csv_file)

# create a list of dictionaries for the issues
issues = []
with open(filepath, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        issues.append(row)
        
url_pieces = github_repo_url.split('/')
project = url_pieces[3]
issue_tracker = url_pieces[4]

repo_id = utils.get_repo_id(project, issue_tracker)
project_details = {}

for issue in issues:
    issue['gh_data'] = utils.create_issue(repo_id, issue['Tasks'])

    project_details['project'] = utils.get_issue_project(project, issue_tracker, issue['gh_data']['number'])
    if not project_details.get('project'):
        print(f"Did not get the project details for #{issue['gh_data']['number']}")
        breakpoint()
        continue

    project_id = project_details['project']['project']['id']
    project_node_id = project_details['project']['id']

    if 'fields' not in project_details:
        fields = utils.get_project_fields(project_id)
        project_details['fields'] = reconcile_fields(fields)

    utils.update_project_fields(project_id, project_node_id, project_details['fields'], issue)
    print(f"Created issue #{issue['gh_data']['number']}")

# TODO: create the User Stories and Requirements
# Use the updated `issues` list to link all tasks to a requirement or user story
print("Done!")