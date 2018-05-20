import requests
from github import Github

def get_commits_for_org(org):
	""" Get all commits for the given org """
	res = {}
	for repo in org.get_repos():
		res[repo.name] = get_commits_for_repo(repo)
	return res

def get_commits_for_repo(repo):
	""" Get all open issues for the given repository """
	res = []
	commits = repo.get_commits()
	i = 0
	for commit in commits:
		# ignore commits that are not associated with a user (e.g. WebFlow commits)
		if not commit.author:
			continue
		commit_entry = {}
		commit_entry['committed_by'] = commit.author.name
		commit_entry['commit_diff'] = get_commit_diff(commit.commit.html_url)
		commit_entry['commit_message'] = commit.commit.message
		res.append(commit_entry)
	return res

def get_commit_diff(commit_url):
	""" Get the diff for this commit
		TODO: find a better way to parse the diff
	"""
	diff_url = commit_url + '.diff'
	resp = requests.get(diff_url)
	return resp.text
