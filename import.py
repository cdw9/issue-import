import csv
import os
from sys import argv
import time

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
        # TODO: normalize the keys. Get user to double check
        issues.append(row)
        
url_pieces = github_repo_url.split('/')
project = url_pieces[3]
issue_tracker = url_pieces[4]

repo_id = utils.get_repo_id(project, issue_tracker)
project_details = {}

for issue in issues[:1]:  # TODO: remove the slice
    issue['gh_data'] = utils.create_issue(repo_id, issue['Tasks'])
    if not project_details:
        project_details['project'] = utils.get_issue_project(project, issue_tracker, issue['gh_data']['number'])
    if not project_details.get('project'):
        breakpoint()
        continue
    project_id = project_details['project']['project']['id']
    project_node_id = project_details['project']['id']
    breakpoint()
    if 'fields' not in project_details:
        project_details['fields'] = utils.get_project_fields(project_id)
    fields = reconcile_fields(project_details['fields'])
    utils.update_project_fields(project_id, project_node_id, fields)
    print(f"Created issue #{issue['gh_data']['number']}")
print("Done!")