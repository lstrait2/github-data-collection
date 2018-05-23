import json
from github import Github
from commits import get_commits_for_org, get_commits_for_repo
from issues import get_issues_for_org, get_issues_for_repo


# get Access Token from user
access_token = input("Please provide a valid user token: ")
# login using an access token
g = Github(access_token)
#org = g.get_organization('cromaLab')
repo = g.get_repo(10270250)
issues = get_issues_for_repo(repo)
#commits = get_commits_for_repo(repo)

with open('data/react/react_issues3.json', 'w') as fp:
    json.dump(issues, fp, indent=4)

#with open('legion_tools_commits.json', 'w') as fp:
    #json.dump(commits, fp, indent=4)