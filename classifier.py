'''

Goal: Build a simple, rules-based classifier that identifies issues that are small, stylistic changes as opposed to larger, more signficant
algorithm or code changes.

'''

def preprocess_issue(issue):
	""" Remove code from issue templates and any other pre-processing that needs done """
	templates = ["Note: if the issue is about documentation or the website, please file it at:"]
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

def classify_issues(issues):
	return [classify_issue(preprocess_issue(issue)) for issue in issues]	


def classify_issue(issue):
	""" returns true if the given issue is a small style/documentation change """
	if not issue['title'] or not issue['body']:
		return False
	return (is_readme_change(issue) or is_documentation_change(issue) or is_labeled_easy(issue) or is_refactor_change(issue) or is_typo_change(issue) or is_deprecated_change(issue))

def is_refactor_change(issue):
	if "refactor" in issue['title']:
		return True
	return False

def is_readme_change(issue):
	if "readme" in issue['title'] or "readme" in issue['body'] or ".md" in issue['title'] or ".md" in issue['body']:
		return True;
	return False

def is_documentation_change(issue):
	if "documentation" in issue['title'] or "documentation" in issue['body'] or "doc" in issue['title'] or "link" in issue['title']:
		return True;
	return False

def is_labeled_easy(issue):
	""" return true if the issue has a label indicating it is a beginner friendly issue
		(e.g. "good first issue" or "Difficulty starter). Note these labels are repository-specific """
	for label in issue['labels']:
		if  "first issue" in label or "starter" in label or "easy" in label:
			return True
	return False

def is_typo_change(issue):
	if "typo" in issue['title'] or "typo" in issue['body']:
		return True;
	return False

def is_deprecated_change(issue):
	if "deprecated" in issue['title']:
		return True
	return False
