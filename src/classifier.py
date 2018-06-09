'''

Goal: Build a simple, rules-based classifier that identifies issues that are small, stylistic changes as opposed to larger, more signficant
algorithm or code changes.

'''

def preprocess_issue(issue):
	""" Remove code from issue templates and any other pre-processing that needs done """
	templates = ["Note: if the issue is about documentation or the website, please file it at:", "Do you want to request a feature or report a bug?", 
	"What is the current behavior?", "What is the expected behavior?", "Which versions of React, and which browser / OS are affected by this issue? Did this work in previous versions of React?"]
	issue_body = issue['body']
	if not issue_body:
		return issue
	for template in templates:
		issue_body = issue_body.replace(template, '')
	issue_body = issue_body.replace('\r', '')
	issue_body = issue_body.replace('\n', '')
	issue['body'] = issue_body.lower()
	issue['title'] = issue['title'].lower()
	return issue

issue_types = {"refactor": 0, "readme":0, "doc":0, "easy":0, "typo":0, "deprecated":0}
def classify_issues(issues):
	labels = [classify_issue(preprocess_issue(issue)) for issue in issues]	
	print(issue_types)
	for key in issue_types:
		issue_types[key] = 0
	return labels

def classify_issue(issue):
	""" returns true if the given issue is a small style/documentation change """
	if not issue['title'] or not issue['body']:
		return False
	return (is_readme_change(issue) or is_documentation_change(issue) or is_labeled_easy(issue) or is_refactor_change(issue) or is_typo_change(issue) or is_deprecated_change(issue))

def is_refactor_change(issue):
	if "refactor" in issue['title']:
		issue_types["refactor"] += 1
		return True
	return False

def is_readme_change(issue):
	if "readme" in issue['title'] or "readme" in issue['body'] or ".md" in issue['title'] or ".md" in issue['body']:
		issue_types["readme"] += 1
		return True
	return False

def is_documentation_change(issue):
	if "documentation" in issue['title'] or "documentation" in issue['body'] or "doc" in issue['title'] or "link" in issue['title']:
		issue_types["doc"] += 1
		return True
	return False

def is_labeled_easy(issue):
	""" return true if the issue has a label indicating it is a beginner friendly issue
		(e.g. "good first issue" or "Difficulty starter). Note these labels are repository-specific """
	for label in issue['labels']:
		if  "first issue" in label['name'] or "starter" in label['name'] or "easy" in label['name']:
			issue_types["easy"] += 1
			return True
	return False

def is_typo_change(issue):
	if "typo" in issue['title'] or "typo" in issue['body']:
		issue_types["typo"] += 1
		return True;
	return False

def is_deprecated_change(issue):
	if "deprecated" in issue['title']:
		issue_types["deprecated"] += 1
		return True
	return False
