with open('data/flutter/flutter_issues_prs.json') as json_data:
    issues_prs = json.load(json_data)

for issue_pr in issues_prs: