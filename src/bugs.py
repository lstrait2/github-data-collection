from bs4 import BeautifulSoup
from urllib.request import urlopen


for bug_id in range(2,3):
	bug_url = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id=' + str(bug_id)
	page = urlopen(bug_url)
	soup = BeautifulSoup(page, 'html.parser')	

	short_desc = soup.select("#short_desc_nonedit_display")[0].text
	long_desc = soup.select(".bz_first_comment")[0].select(".bz_comment_text")[0].text
	status = soup.select("#static_bug_status")[0].text
	product = soup.select("#field_container_product")[0].text
	component = soup.select("#field_container_component")[0].text
	duplicates = soup.select("#duplicates")[0].select("a")[0]['href']
	#TODO: select only the date/time here
	created_at = soup.select("#bz_show_bug_column_2")[0].select("td")[0].text
	print(duplicates)


	#TODO: scrape the page with the updates, need to find who marked as resolved
	#TODO: also need to get the date/time it was marked as fixed
	#TODO: handle duplicates same way as well.
	bug_history_url = 'https://bugs.eclipse.org/bugs/show_activity.cgi?id=' + str(bug_id)
	page = urlopen(bug_history_url)
	soup = BeautifulSoup(page, 'html.parser')	
	data = []
	table = soup.find('table', attrs={'id':'bug_activity'})
	#print(table)
	table_body = table.find('tbody')
	rows = table.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele]) # Get rid of empty values
	#print(data)