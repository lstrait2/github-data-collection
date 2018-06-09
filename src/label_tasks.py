import json
import requests

def find_closing_pr(issue_id, prs):
	""" Find the PR(s) that reference the given issue. That is it cotains "#{issue_id}" in its title or body """
	issue_id_string = "#" + str(issue_id)
	ret = []
	for pr in prs:
		if issue_id_string in pr['title'] or issue_id_string in pr['body']:
			# only want to consider PRs that were merged into master
			# TODO: move this enrichment of PR data somewhere else...
			pr_details = requests.get(pr['pull_request']['url']).json()
			if pr_details['merged']:
				ret.append(pr['id'])
	return ret

#def find_closing_commit(issue):

with open('data/react/react_pulls_open.json') as json_data:
    prs = json.load(json_data)

print(find_closing_pr(6723, prs))
 