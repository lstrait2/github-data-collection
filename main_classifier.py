import json

from classifier import classify_issues

with open('data/react/react_issues.json') as f:
    issues = json.load(f)

labels = classify_issues(issues)

for i, label in enumerate(labels):
	if label:
		print(issues[i]['title'])