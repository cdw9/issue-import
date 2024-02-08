import csv
import os
from sys import argv

import utils

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

for issue in issues[:1]:
    issue['gh_id'] = utils.create_issue(repo_id, issue['Tasks'])
    if not project_details:
        project_details = utils.get_issue_metadata(project, issue_tracker, issue['gh_id'])
    # now populate the fields