from github import Github
from issues import get_issues_for_org

# get Access Token from user
access_token = input("Please provide a valid user token: ")
# login using an access token
g = Github(access_token)
# get all isssues and commits for cromaLab Org
org = g.get_organization('cromaLab')
print(get_issues_for_org(org))