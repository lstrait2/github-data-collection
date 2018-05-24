import json
from github import Github
from commits import get_commits_for_org, get_commits_for_repo
from issues import get_issues_for_org, get_issues_for_repo


# get Access Token from file
with open("token.txt", "r") as token_file:
	access_token = token_file.read().strip()

# login using an access token
g = Github(access_token)

#org = g.get_organization('cromaLab')
repo = g.get_repo(10270250)
issues = get_issues_for_repo(g, repo)
#commits = get_commits_for_repo(repo)

with open('data/react/react_issues9.json', 'w') as fp:
    json.dump(issues, fp, indent=4)