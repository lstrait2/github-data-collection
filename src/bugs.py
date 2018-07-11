import json
import time
from bs4 import BeautifulSoup
#from urllib.request import urlopen
import requests

issues = []
for bug_id in range(275000,325000):
	print("getting issue: #" + str(bug_id))
	bug_url = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id=' + str(bug_id)
	for i in range(0,10):
		try:
			page = requests.get(bug_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}).text
		except:
			print("connection failed")
			time.sleep(60)
			continue
		break
	soup = BeautifulSoup(page, 'html.parser')	
	short_desc = soup.select("#short_desc_nonedit_display")
	# if not a valid bug, move onto the next
	if not short_desc:
		continue
	short_desc = short_desc[0].text
	long_desc = soup.select(".bz_first_comment")[0].select(".bz_comment_text")[0].text
	status = soup.select("#static_bug_status")[0].text
	product = soup.select("#field_container_product")[0].text
	component = soup.select("#field_container_component")[0].text
	duplicates = []
	duplicates_div = soup.select("#duplicates")
	if duplicates_div:
		for duplicate in duplicates_div[0].select("a"):
			duplicates.append(duplicate.text)
	#TODO: select only the date/time here
	created_at = soup.select("#bz_show_bug_column_2")[0].select("td")[0].text

	# scrape the page with the updates, need to find who marked as fixed and when
	bug_history_url = 'https://bugs.eclipse.org/bugs/show_activity.cgi?id=' + str(bug_id)
	for i in range(0,10):
	    try:
	        page = requests.get(bug_history_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}).text
	    except:
	    	print("connection failed")
	    	time.sleep(60)
	    	continue
	    break
	soup = BeautifulSoup(page, 'html.parser')	
	data = []
	table = soup.find('table', attrs={'id':'bug_activity'})
	if not table:
		continue
	table_body = table.find('tbody')
	rows = table.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele]) # Get rid of empty values
	#TODO: Two possible ways for the bug to be marked done (make sure this works)
	completed_by = None
	completed_time = None
	for idx, row in enumerate(data):
		if len(row) > 4 and row[4] == 'RESOLVED' and (idx + 1) < len(data) and len(data[idx+1]) > 2 and data[idx+1][2] == 'FIXED':
			completed_by = row[0]
			completed_time = row[1]
			break

	issue = {}
	issue['issue_id'] = bug_id
	issue['short_desc'] = short_desc
	issue['long_desc'] = long_desc
	issue['component'] = component
	issue['product'] = product
	issue['duplicates'] = duplicates
	issue['completed_by'] = completed_by
	issue['completed_at'] = completed_time
	issue['created_at'] = created_at
	issues.append(issue)

with open('data/eclipse/eclpise_issues14.json', 'w') as f:
    json.dump(issues, f, indent=4)

