import json
import re
import requests

from time import sleep


def get_commits_query(repo):
	""" Returns list containing all commits in the given repo  """
	commits = []
	date = '2000-01-01'
	headers = {"Accept":"application/vnd.github.cloak-preview"}
	# Search API can only return 1000 results at a time, so need to break calls apart by time period
	while True:
		print(date)
		# commit search API in preview/testing phase, must specify accept header to access
		r = requests.get('https://api.github.com/search/commits?q=%22%22+repo:%s+committer-date:>%s&sort=committer-date&order=asc' % (repo,date), headers=headers)
		# no more issues to collect, write to file and return
		if r.json()['total_count'] == 0:
			return commits
		commits.extend(r.json()['items'])
		if 'Link' not in r.headers:
			return commits
		next_page, last_page = re.findall(r'\<(.*?)\>', r.headers['Link'])
		print(next_page)
		print(last_page)
		page = 2
		while next_page != last_page:
			# sleep for a minute every 9 pages to avoid rate limiting
			if page % 9 == 0:
				sleep(60)
			r = requests.get(next_page, headers=headers)
			if (len(r.json()['items']) == 0):
				print("retrying request")
				page += 1
				continue
			commits.extend(r.json()['items'])
			_, next_page, _ , _ = re.findall(r'\<(.*?)\>', r.headers['Link'])
			page += 1
		r = requests.get(last_page, headers=headers)
		commits.extend(r.json()['items'])
		date = commits[-1]['commit']['committer']['date'][:10]
		# sleep before next iteration to avoid rate limiting
		sleep(60)

commits = get_commits_query("pytorch/torch")
with open('data/pytorch/pytorch_commits.json', 'w') as f:
    json.dump(commits, f, indent=4)