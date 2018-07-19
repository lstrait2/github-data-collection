import json
with open('data/flutter/flutter_issues_prs_temp.json') as json_data:
	issues_prs = json.load(json_data)
for issue_pr in issues_prs:
	remove_commits = []
	for commit in issue_pr['local_commits']:
		if commit['author'] not in commit['commit']:
			issue_pr['master_commits'].append(commit)
			remove_commits.append(commit)
	for commit in remove_commits:
		issue_pr['local_commits'].remove(commit)
with open('data/flutter/issues_prs_temp.json', 'w') as f:
    json.dump(issues_prs, f, indent=4)

