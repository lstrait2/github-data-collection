import json
import re
import requests
from requests.auth import HTTPBasicAuth

def get_author_pr(pr_url):
	# pr_url looks like '/flutter/flutter/pull/297'
	pr_url = pr_url.replace('pull', 'pulls')
	r = requests.get('https://api.github.com/repos' + pr_url, auth=HTTPBasicAuth('user', 'pass')).json()
	if 'user' not in r:
		return None, False
	return r['user']['login'], r['merged']

with open('data/flutter/issues_prs.json') as json_data:
    issues_prs = json.load(json_data)

for issue_pr in issues_prs[10000:]:
	print(issue_pr['issue_num'])
	remove_prs = []
	for pr in issue_pr['merged_prs']:
		author, is_merged = get_author_pr(pr['pull'])
		if not pr['author']:
			pr['author'] = author
		if not is_merged:
			remove_prs.append(pr)
	for pr in remove_prs:
		issue_pr['merged_prs'] = list(filter(lambda x: x != pr, issue_pr['merged_prs']))
		issue_pr['failed_prs'].append(pr)
	for pr in issue_pr['failed_prs']:
		if not pr['author']:
			pr['author'] = get_author_pr(pr['pull'])[0]
	for commit in issue_pr['master_commits']:
		if not commit['author']:
			print("found unauthored commit " + commit)
	for commit in issue_pr['local_commits']:
		if not commit['author']:
			print("found unauthored commit " + commit)

with open('data/flutter/flutter_issues_prs_10.json', 'w') as f:
    json.dump(issues_prs[10000:], f, indent=4)