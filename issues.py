from github import Github


def get_issues_for_org(org):
	""" Get all open issues for the given org """
	res = {}
	for repo in org.get_repos():
		res[repo.name] = get_issues_for_repo(repo)
	return res
		
def get_issues_for_repo(g, repo):
	""" Get all closed issues for the given repository """
	res = []
	# Note: must specify type:issue or this query will also return PRs!!!
	issues = g.search_issues(query='', **{'repo':'facebook/react', 'type':'issue'})
	#issues = repo.get_issues(state='closed')
	for issue in issues[:2000]:
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
