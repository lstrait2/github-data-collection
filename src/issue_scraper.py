import json
import time
import requests
from bs4 import BeautifulSoup
 
issues = []
for issue_num in range(1000,19479):
	if issue_num % 100 == 0:
		time.sleep(30)
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
	#timeline = soup.select(".js-timeline-item")[0].findChildren(recursive=False)
	timeline = soup.select(".discussion-item")
	merged_prs = []
	failed_prs = []
	master_commits = []
	local_commits = []
	for event in timeline:
		# break if this is where the issue is closed
		if len(event.get('class')) > 1 and event.get('class')[1] == 'discussion-item-closed':
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
			author = event.select(".author")
			#TODO: need to handle Null authors after
			if author:
				author = author[0].text
			else:
				author = None
			d = {"pull": title, "author": author}
			state = event.select(".State")[0].text.strip()
			if state == "Merged":
				merged_prs.append(d)
			else:
				failed_prs.append(d)
	# try to find PRs from comments on the issue
	comments = soup.select(".js-comment-container")
	comment_links = []
	for comment in comments:
		comment_links.extend(comment.select(".issue-link"))
	for link in comment_links:
		link = link['href'].replace("https://github.com", "")
		if "pull" in link and link not in merged_prs:
			d = {"pull":link, "author":None}
			merged_prs.append(d)
	issue = {}
	issue['issue_num'] = issue_num
	issue['merged_prs'] = merged_prs
	issue['failed_prs'] = failed_prs
	issue['master_commits'] = master_commits
	issue['local_commits'] = local_commits
	issues.append(issue)
with open('data/flutter/issues_prs_2.json', 'w') as f:
    json.dump(issues, f, indent=4)
print(issues)