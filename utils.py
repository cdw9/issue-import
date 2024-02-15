import requests
from env import accesstoken

HEADERS = {
    "Authorization": f"Bearer {accesstoken}"
}
BASE_URL = "https://api.github.com/graphql"

def error_handling(response, e):
    # provide some details and a breakpoint for debugging
    print("There was an error!")
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
    print(response.text)
    print(e)
    breakpoint()

def get_repo_id(owner, name):
    # return the repository ID, it is needed for creating issues
    query = f"""
        query {{
            repository(owner: "{owner}", name: "{name}") {{
                id
            }}
        }}
        """
    response = requests.post(BASE_URL, json={"query": query}, headers=HEADERS)
    try:
        return response.json()['data']['repository']['id']
    except Exception as e:
        error_handling(response, e)

def create_issue(repo_id, title):
    # create an issue in the repository, return the Issue data
    query = f"""
        mutation {{
            createIssue(
                input: {{
                    repositoryId: "{repo_id}",
                    title: "{title}",
                    body: ""
                }}
            ) {{
                issue {{
                    id
                    number
                    title
                    bodyText
                }}
            }}
        }}
    """
    response = requests.post(BASE_URL, json={"query": query}, headers=HEADERS)
    try:
        return response.json()['data']['createIssue']['issue']
        # issue contains id, number, title, bodyText
    except Exception as e:
        error_handling(response, e)

def get_issue_project(project, issue_tracker, issue_number, tries=0):
    # take the issue information, return the first project ID
    # if the issue is not in a project, return None
    query = f"""
        query {{
            repository(owner:"{project}", name:"{issue_tracker}") {{
                issue(number:{issue_number}) {{
                    id
                    projectItems(first:5) {{
                        nodes {{
                            id
                            project {{
                                id
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
    response = requests.post(BASE_URL, json={"query": query}, headers=HEADERS)
    response_data = response.json()
    try:
        # query until we get project data, becasue it may not be there yet
        if not response_data['data']['repository']['issue']['projectItems']['nodes']:
            tries += 1
            if tries > 10:
                print(f"Issue #{issue_number} is not in a project yet, it will need to be manually updated")
                return None
            return get_issue_project(project, issue_tracker, issue_number, tries)
    except Exception as e:
        error_handling(response, e)
    return response_data['data']['repository']['issue']['projectItems']['nodes'][0]

def get_project_fields(project_id):
    # return the fields for the project
    query = f"""
        query {{
            node(id: "{project_id}") {{
                ... on ProjectV2 {{
                    fields(first: 20) {{
                        nodes {{
                            ... on ProjectV2Field {{
                                id
                                name
                            }}
                            ... on ProjectV2IterationField {{
                                id
                                name
                                configuration {{
                                    iterations {{
                                        startDate
                                        id
                                    }}
                                }}
                            }}
                            ... on ProjectV2SingleSelectField {{
                                id
                                name
                                options {{
                                    id
                                    name
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
    response = requests.post(BASE_URL, json={"query": query}, headers=HEADERS)
    try:
        return response.json()['data']['node']['fields']['nodes']
    except Exception as e:
        error_handling(response, e)

def update_project_fields(project_id, issue_id, fields, row):
    # Update the project fields
    # Component and Effort Planned from the CSV
    # Other defaults as set in fields.py
    for field in fields:
        if fields[field]['type'] == 'Number':
            # only two number fields (Complexity and Effort Planned) get the same value
            try:
                fields[field]['value'] = float(list(row.values())[4])
            except Exception as e:
                # might be a key error, or the value isn't a number
                continue
            mutation_query = f"""
                mutation {{
                    updateProjectV2ItemFieldValue(
                        input: {{
                            projectId: "{project_id}"
                            itemId: "{issue_id}"
                            fieldId: "{fields[field]['id']}"
                            value: {{
                                number: {fields[field]['value']}
                            }}
                        }}
                    )
                    {{
                        projectV2Item {{
                            id
                        }}
                    }}
                }}
            """
            response = requests.post(BASE_URL, json={"query": mutation_query}, headers=HEADERS)
            if response.status_code != 200 or 'errors' in response.json():
                error_handling(response, '')

        elif fields[field]['type'] == 'Single Select':
            field_value = ""
            if field == 'Component':
                field_value = fields[field]['options'][row['Component']]
            elif field == 'Job Code':
                if len(fields[field]['options']) == 1:
                    field_value = list(fields[field]['options'].values())[0]
            if 'default_id' in fields[field]:
                field_value = fields[field]['default_id']
            if not field_value:
                continue

            mutation_query = f"""
                mutation {{
                    updateProjectV2ItemFieldValue(
                        input: {{
                            projectId: "{project_id}"
                            itemId: "{issue_id}"
                            fieldId: "{fields[field]['id']}"
                            value: {{
                                singleSelectOptionId: "{field_value}"
                            }}
                        }}
                    )
                    {{
                        projectV2Item {{
                            id
                        }}
                    }}
                }}
            """
            response = requests.post(BASE_URL, json={"query": mutation_query}, headers=HEADERS)
            if response.status_code != 200 or 'errors' in response.json():
                error_handling(response, '')

        elif fields[field]['type'] == 'Text':
            field_value = ""
            if field == 'User Story':
                field_value = row['User Story']
            if not field_value:
                continue

            mutation_query = f"""
                mutation {{
                    updateProjectV2ItemFieldValue(
                        input: {{
                            projectId: "{project_id}"
                            itemId: "{issue_id}"
                            fieldId: "{fields[field]['id']}"
                            value: {{
                                text: "{field_value}"
                            }}
                        }}
                    )
                    {{
                        projectV2Item {{
                            id
                        }}
                    }}
                }}
            """
            response = requests.post(BASE_URL, json={"query": mutation_query}, headers=HEADERS)
            if response.status_code != 200 or 'errors' in response.json():
                error_handling(response, '')