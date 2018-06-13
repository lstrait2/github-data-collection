import json
import os
import re
import requests

from time import sleep


def get_pulls_query(repo, state):
	""" Returns list containing all pulls in the given repo with state """
	issues = []
	date = '2000-01-01'
	# Search API can only return 1000 results at a time, so need to break calls apart by time period
	while True:
		r = requests.get('https://api.github.com/search/issues?q=%22%22+repo:%s+type:pr+state:%s+created:>%s&sort=created&order=asc' % (repo,state,date))
		# no more issues to collect, write to file and return
		if r.json()['total_count'] == 0:
			return issues
		issues.extend(r.json()['items'])
		if 'Link' not in r.headers:
			return issues
		next_page, last_page = re.findall(r'\<(.*?)\>', r.headers['Link'])
		page = 2
		while next_page != last_page:
			# sleep for a minute every 9 pages to avoid rate limiting
			if page % 9 == 0:
				sleep(60)
			r = requests.get(next_page)
			issues.extend(r.json()['items'])
			_, next_page, _ , _ = re.findall(r'\<(.*?)\>', r.headers['Link'])
			page += 1
		r = requests.get(last_page)
		issues.extend(r.json()['items'])
		date = issues[-1]['created_at'][:10]
		# sleep before next iteration to avoid rate limiting
		sleep(60)


def get_comments_for_pulls(prs):
	for pr in prs[2500:]:
		comments = requests.get(pr['comments_url'], auth=(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])).json()
		pr['comments'] = comments
	with open('data/flutter/flutter_pulls_comments_2.json', 'w') as f:
		json.dump(prs, f, indent=4)


'''
issues = get_pulls_query('flutter/flutter', 'closed')
with open('data/flutter/flutter_pulls_closed.json', 'w') as f:
    json.dump(issues, f, indent=4)
'''
with open('data/flutter/flutter_pulls_closed.json') as json_data:
    prs = json.load(json_data)
get_comments_for_pulls(prs)