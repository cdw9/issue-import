import requests
from env import accesstoken

headers = {
    "Authorization": f"Bearer {accesstoken}"
}
base_url = "https://api.github.com/graphql"

def get_repo_id(owner, name):
    # return the repository ID, it is needed for creating issues
    query = f"""
        query {{
            repository(owner: "{owner}", name: "{name}") {{
                id
            }}
        }}
        """
    response = requests.post(base_url, json={"query": query}, headers=headers)
    try:
        return response.json()['data']['repository']['id']
    except KeyError:
        print("There was an error!")
        breakpoint()

def create_issue(repo_id, title):
    # create an issue in the repository
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
    response = requests.post(base_url, json={"query": query}, headers=headers)
    try:
        return response.json()['data']['createIssue']['issue']['id']
    except KeyError:
        print("There was an error!")
        breakpoint()

def get_issue_metadata(project, issue_tracker, issue_id):
    # take the issue information, builds a query to return:
    # - IDs of all projects the issue is in
    # - Field information so we can populate things like Time Remaining and Component
    query = f"""
        query {{
            repository(owner:"{project}", name:"{issue_tracker}") {{
                issue(id:{issue_id}) {{
                    id
                    projectItems(first:5) {{
                        nodes {{
                            id
                            project {{
                                id
                            }}
                            fieldValues(last: 13) {{
                                nodes {{
                                    ... on ProjectV2ItemFieldNumberValue {{
                                        id
                                        number
                                        field {{
                                            ... on ProjectV2FieldCommon {{
                                                id
                                                name
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
    response = requests.post(base_url, json={"query": query}, headers=headers)
    response_data = response.json()
    try:
        return response_data['data']['repository']['issue']
    except KeyError:
        print("There was an error!")
        breakpoint()
