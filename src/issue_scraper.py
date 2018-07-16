import json
import time
import requests
from bs4 import BeautifulSoup
 
issues = []
for issue_num in range(1,100):
	print("getting issue: #" + str(issue_num))
	issue_url = 'https://github.com/flutter/flutter/issues/' + str(issue_num)
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
	if soup.select(".pull-request-tab-content"):
		continue
	# get all immediate children
	timeline = soup.select(".js-timeline-item")[0].findChildren(recursive=False)
	merged_prs = []
	failed_prs = []
	master_commits = []
	local_commits = []
	for event in timeline:
		# break if this is where the issue is closed
		if event.get('class')[0] == 'closed-banner':
			break
		# get any commits for the issue
		if len(event.get('class')) > 1 and event.get('class')[1] == 'discussion-commits':
			commit = event.select(".message")[0]['href']
			author = event.select(".author")[0].text
			d = {"commit": commit, "author":author}
			if root in commit:
				master_commits.append(d)
			else:
				local_commits.append(d)
		# get any prs for the issue
		title = event.select(".discussion-item-ref-title")
		if len(title) != 0:
			title = title[0].select("a")[0]['href']
		else:
			title = ""
		if "pull" in title:
			author = event.select(".author")[0].text
			d = {"pull": title, "author":author}
			state = event.select(".State")[0].text.strip()
			if state == "Merged":
				merged_prs.append(d)
			else:
				failed_prs.append(d)
	issue = {}
	issue['issue_num'] = issue_num
	issue['merged_prs'] = merged_prs
	issue['failed_prs'] = failed_prs
	issue['master_commits'] = master_commits
	issue['local_commits'] = local_commits
	issues.append(issue)
with open('data/flutter/flutter/issues_prs_1.json', 'w') as f:
    json.dump(issues, f, indent=4)
print(issues)