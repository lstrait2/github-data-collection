import json
import os
import re
import requests


def label_issues(issues, all_prs):
	for issue in issues[:1000]:
		issue['training_labels'] = {}
		assignees = get_assignees(issue)
		if assignees == []:
			continue
		prs = find_closing_pr(issue['number'], all_prs)
		print(len(prs))
		prs += find_closing_prs_comments(issue['number'], all_prs)
		print(len(prs))
		issue['matching_prs'] = prs
		commits = find_closing_commit(issue)
		print(len(commits))
		issue['matching_commits'] = commits
		assignees = get_assignees(issue)
		for assignee in assignees:
			print(assignee)
			label = 0
			for commit in commits:
				if 'author' in commit:
					print("c: " + commit['author']['login'])
				if commit and 'author' in commit and assignee == commit['author']['login']:
					label = 1
			for pr in prs:
				print("p: " + pr["user"]["login"])
				if pr and assignee == pr['user']['login']:
					label = 1
			print(issue['url'])
			issue['training_labels'][assignee] = label
			print(issue['training_labels'])
	#TODO: write out to labeled file
	with open('data/flutter/flutter_issues_labeled_1.json', 'w') as f:
		json.dump(issues, f, indent=4)

def label_issues_comments(issues, prs_comments):
	for issue in issues:
		prs = find_closing_prs_comments(issue['number'], prs_comments)
		if prs != []:
			if 'matching_prs' in issue:
				print(len(issue['matching_prs']))
				issue['matching_prs'] += prs
				print(len(issue['matching_prs']))
			else:
				issue['matching_ptrs'] = prs
		assignees = issue['training_labels'].keys()
		for assignee in assignees:
			#print(assignee)
			label = 0
			for pr in prs:
				print("p: " + pr["user"]["login"])
				if pr and assignee == pr['user']['login']:
					label = 1
				print(issue['url'])
				print(issue['training_labels'])
				issue['training_labels'][assignee] = max(issue['training_labels'][assignee], label)
				print(issue['training_labels'])
	with open('data/flutter/flutter_issues_labeled_2.json', 'w') as f:
		json.dump(issues, f, indent=4)


def find_closing_prs_comments(issue_id, prs):
	ret = [] 
	issue_id_string = "#" + str(issue_id)
	issue_id_string2 = "/" + str(issue_id) 
	for pr in prs:
		for comment in pr['comments']:
			print(comment)
			print(re.search(issue_id_string2 + r'(?!\d)', comment['body']))
			if comment['body'] and (re.search(issue_id_string + r'(?!\d)', comment['body']) or re.search(issue_id_string2 + r'(?!\d)', comment['body'])):
				if 'pull_request' not in pr:
					pr_details = pr
				else:
					pr_details = requests.get(pr['pull_request']['url'], auth=(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])).json()
				# only want to consider PRs that were merged into master
				if pr_details['merged'] and pr_details not in ret:
					ret.append(pr_details)
	return ret


def find_closing_pr(issue_id, prs):
	""" Find the PR(s) that reference the given issue. That is it cotains "#{issue_id}" in its title or body """
	ret = []
	issue_id_string = "#" + str(issue_id) 
	issue_id_string2 = "/" + str(issue_id)
	for pr in prs:
		# for regex, don't want #123 to match issues with same prefix (#1234)
		if re.search(issue_id_string + r'(?!\d)', pr['title']) or (pr['body'] and re.search(issue_id_string + r'(?!\d)', pr['body'])) or (pr['body'] and re.search(issue_id_string2 + r'(?!\d)', pr['body'])):
			if 'pull_request' not in pr:
				pr_details = pr
			else:
				pr_details = requests.get(pr['pull_request']['url'], auth=(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])).json()
			# only want to consider PRs that were merged into master
			if pr_details['merged']:
				ret.append(pr_details)
	return ret


def find_closing_commit(issue):
	""" Find the commit that closes the given issue. That is a commit (for master branch) event exists for the issue """
	ret = []	
	#TODO: move this enrichment of issue data somewhere else...
	events= requests.get(issue['events_url'], auth=(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])).json()
	for event in events:
		# make sure this event is a commit and that it is for the master branch of this project
		if event['commit_id'] and get_repo_commit(event['commit_url']) == get_repo_event(event['url']):
			commit_details = requests.get(event['commit_url'], auth=(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])).json()
			ret.append(commit_details)
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
	events= requests.get(issue['events_url'], auth=(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])).json()
	for event in events:
		if event['event'] == "assigned":
			assignees.append(event['assignee']['login'])
	return assignees



with open('data/flutter/flutter_pulls_closed.json') as json_data:
    prs = json.load(json_data)
with open('data/flutter/flutter_issues_closed.json') as json_data:
	issues = json.load(json_data)
with open('data/tensorflow/tensorflow_issues_closed.json') as json_data_tf:
	issues_tf = json.load(json_data_tf)
with open('data/tensorflow/tensorflow_pulls_closed.json') as json_data:
    prs_tf = json.load(json_data)

with open('data/flutter/flutter_pulls_comments.json') as json_data:
    prs_comments = json.load(json_data)
with open('data/flutter/flutter_issues_labeled.json') as json_data:
	labeled_issues = json.load(json_data)
temp_issue = None
for issue in labeled_issues:
	if issue['number'] == 140:
		temp_issue = issue
		break
temp_pr = None
for pr in prs_comments:
	if pr['number'] == 830:
		temp_pr = pr
		break

print(label_issues([temp_issue], [temp_pr]))
#print(label_issues(issues, prs_comments))

#print(find_closing_commit(temp_issue))
#print(find_closing_pr(6723, prs))
'''
temp_issue_tf = None
for issue in issues_tf:
	if issue['number'] == 18477:
		temp_issue_tf = issue
		break
'''
#print(get_assignees(temp_issue_tf))