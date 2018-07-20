import json
import time
import requests
from bs4 import BeautifulSoup



with open('data/flutter/flutter_issues_prs_final_3.json') as json_data:
    issues_prs = json.load(json_data)

for issue_pr in issues_prs:
	for commit in issue_pr['master_commits']:
		print(issue_pr['issue_num'])
		issue_url = 'https://github.com' + commit['commit']
		for i in range(0,10):
			try:
				page = requests.get(issue_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}).text
			except:
				print("connection failed")
				time.sleep(60)
				continue
			break
		soup = BeautifulSoup(page, 'html.parser')
		meta = soup.select('.commit-meta')[0]
		links = meta.select('.flex-auto')[0].select('a')
		author = links[0].text
		print(author)
		commit['author'] = author

with open('data/flutter/flutter_issues_prs_final_4.json', 'w') as f:
    json.dump(issues_prs, f, indent=4)
