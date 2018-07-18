import json
import time
import requests
from bs4 import BeautifulSoup
 
issues_prs = [{'issue_num': 231, 'merged_prs': [], 'failed_prs': [], 'master_commits': [], 'local_commits': [{'commit': '/abarth/flutter/commit/e47cee5b9f35acca45293da4773c03a3e88ca98a', 'author': 'abarth'}]},
{'issue_num': 371, 'merged_prs': [], 'failed_prs': [], 'master_commits': [], 'local_commits': [{'commit': '/collinjackson/flutter/commit/8c195c074f1ac1786946dacabc1d666c3efbe30d', 'author': 'collinjackson'}]},
{'issue_num': 1443, 'merged_prs': [], 'failed_prs': [], 'master_commits': [], 'local_commits': [{'commit': '/collinjackson/flutter/commit/933a893668476ace181187479c916fe5c2717be2', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/0e83bf60875dc981f3572f31c0542ee1c4d6075a', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/709ab28dd4f3759ab4336982121d45949963ed4f', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/5087a8118c87e101cc032b3ebb234afaf806ad2a', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/cfcdff65ee2623461873c1bb45ccbdd5367e136c', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/36e029633a9f12abbb63cc313b8b0db8fe748beb', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/4aa26a09da97f08d865e8c9b92d4948aba53bb40', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/0eda7228a0e325b7344374a04a67f6535956c630', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/6e036f2ee8d2a9d5fec15db7482fdb2817eaacb0', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/5f9b0e5f81d2c2fe0c970a2a7265b4acff3a2293', 'author': 'collinjackson'}, {'commit': '/collinjackson/flutter/commit/ddf0082af42bab9fb56e86232b9a86c3f7f7464a', 'author': 'collinjackson'}]}]
for issue_pr in issues_prs:
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
	if soup.select(".pull-request-tab-content"):
		continue
	# get all immediate children
	closed = soup.select(".discussion-item-closed")[0]
	closed_text = closed.text.replace(" ", "").replace("\n", "")
	if "closedthisin" in closed_text:
		print(closed.select("code")[0].select("a")[0]['href'])
#with open('data/flutter/issues_prs_2.json', 'w') as f:
    #json.dump(issues_prs, f, indent=4)