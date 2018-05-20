import json
from github import Github
from commits import get_commits_for_org, get_commits_for_repo
from issues import get_issues_for_org, get_issues_for_repo


# get Access Token from user
access_token = input("Please provide a valid user token: ")
# login using an access token
g = Github(access_token)
# get all isssues and commits for cromaLab Org
org = g.get_organization('cromaLab')
repo = org.get_repo("LegionTools")
issues = get_issues_for_repo(repo)
commits = get_commits_for_repo(repo)

with open('legion_tools_issues.json', 'w') as fp:
    json.dump(issues, fp, indent=4)

with open('legion_tools_commits.json', 'w') as fp:
    json.dump(commits, fp, indent=4)