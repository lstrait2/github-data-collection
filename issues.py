from github import Github

'''
NOTE MUST USE PYTHON3
'''

# get Access Token from user
access_token = input("Please provide a valid user token: ")
# login using an access token
g = Github(access_token)

org = g.get_organization('cromaLab')
repo = org.get_repo('Onboarding')
issues = repo.get_issues()

for issue in issues:
	print(issue.body)




#file_contents = repo.get_file_contents('path/to/file')