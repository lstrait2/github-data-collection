from github import Github


def get_issues_for_org(org):
	""" Get all open issues for the given org """
	res = {}
	for repo in org.get_repos():
		res[repo.name] = get_issues_for_repo(repo)
	return res
		
def get_issues_for_repo(repo):
	""" Get all closed issues for the given repository """
	res = []
	issues = repo.get_issues(state='closed')
	i = 0
	for issue in issues[1999:3000]:
		print(i)
		i += 1
		issue_entry = {}
		issue_entry['title'] = issue.title
		issue_entry['created_by'] = issue.user.name
		issue_entry['body'] = issue.body
		issue_entry['labels'] = [label.name for label in issue.labels]
		#issue_entry['comments'] = get_comments_for_issue(issue)
		res.append(issue_entry)
	return res

def get_comments_for_issue(issue):
	""" Get all comments for the given issue """
	res = []
	for comment in issue.get_comments():
		comment_entry = {}
		comment_entry['created_by'] = comment.user.name
		comment_entry['body'] = comment.body
		res.append(comment_entry)
	return res
