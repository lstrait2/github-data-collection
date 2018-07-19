import json
import time
import requests
from bs4 import BeautifulSoup
 
with open('data/flutter/flutter_issues_prs.json') as json_data:
    issues_prs = json.load(json_data)

for issue_pr in issues_prs:
	print(issue_pr['issue_num'])
	if issue_pr['issue_num'] % 300 == 0:
		time.sleep(15)
	issue_url = 'https://github.com/flutter/flutter/issues/' + str(issue_pr['issue_num'])
	root = "/flutter/flutter"
	for i in range(0,10):
		try:
			page = requests.get(issue_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}).text
		except:
			print("connection failed")
			time.sleep(60)
			continue
		break
	soup = BeautifulSoup(page, 'html.parser')
	# looking at a PR and not an issue
	if soup.select(".pull-request-tab-content") or len(soup.select(".discussion-item-closed")) == 0:
		continue
	# get all immediate children
	if len(soup.select(".discussion-item-closed")) == 0:
		print("closing")
		continue
	closed = soup.select(".discussion-item-closed")[0]
	if len(closed.select(".author")) == 0 or not closed.select(".author")[0].has_attr('href'):
		print("closing2")
		continue
	author = closed.select(".author")[0]['href']
	closed_text = closed.text.replace(" ", "").replace("\n", "")
	if "closedthisin" in closed_text:
		if len(closed.select("code")) > 0:
			print(closed_text)
			closing_commit = closed.select("code")[0].select("a")[0]['href']
			d = {}
			d['commit'] = closing_commit
			d['author'] = author
			issue_pr['master_commits'].append(d)

with open('data/flutter/issues_prs_temp.json', 'w') as f:
    json.dump(issues_prs, f, indent=4)