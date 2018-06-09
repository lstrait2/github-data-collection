import json
import requests

def find_closing_pr(issue_id, prs):
	""" Find the PR(s) that reference the given issue. That is it cotains "#{issue_id}" in its title or body """
	ret = []
	issue_id_string = "#" + str(issue_id)
	for pr in prs:
		if issue_id_string in pr['title'] or issue_id_string in pr['body']:
			# only want to consider PRs that were merged into master
			# TODO: move this enrichment of PR data somewhere else...
			pr_details = requests.get(pr['pull_request']['url']).json()
			if pr_details['merged']:
				ret.append(pr['id'])
	return ret

def find_closing_commit(issue):
	""" Find the commit that closes the given issue. That is a commit (for master branch) event exists for the issue """
	ret = []
	#TODO: move this enrichment of issue data somewhere else...
	events= requests.get(issue['events_url']).json()
	for event in events:
		# make sure this event is a commit and that it is for the master branch of this project
		if event['commit_id'] and get_repo_commit(event['commit_url']) == get_repo_event(event['url']):
			ret.append(event['commit_id'])
	return ret

def get_repo_commit(commit_url):
	""" Helper method to strip out repo name from a commit event url """
	commit_repo = commit_url.replace("https://api.github.com/repos/", "")
	return commit_repo[:commit_repo.index("/commits")]

def get_repo_event(event_url):
	""" Helper method to strip out repo name from a commit event url """
	event_repo = event_url.replace("https://api.github.com/repos/", "")
	return event_repo[:event_repo.index("/issues")]


def get_assignees(issue):
	""" Return a list of all individuals who had been assigned to a task, in the order they were assigned """
	assignees = []
	#TODO: move this enrichment of issue data somewhere else...
	events= requests.get(issue['events_url']).json()
	for event in events:
		if event['event'] == "assigned":
			assignees.append(event['assignee']['login'])
	return assignees



with open('data/react/react_pulls_open.json') as json_data:
    prs = json.load(json_data)
with open('data/react/react_issues_closed.json') as json_data:
	issues = json.load(json_data)
with open('data/tensorflow/tensorflow_issues_closed.json') as json_data_tf:
	issues_tf = json.load(json_data_tf)
temp_issue = None
for issue in issues:
	if issue['number'] == 11257:
		temp_issue = issue
		break
print(temp_issue)
print(find_closing_commit(temp_issue))
#print(find_closing_pr(6723, prs))
temp_issue_tf = None
for issue in issues_tf:
	if issue['number'] == 18477:
		temp_issue_tf = issue
		break
print(get_assignees(temp_issue_tf))