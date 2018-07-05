from bs4 import BeautifulSoup
from urllib.request import urlopen


for bug_id in range(1,2):
	bug_url = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id=' + str(bug_id)
	page = urlopen(bug_url)
	soup = BeautifulSoup(page, 'html.parser')	

	short_desc = soup.select("#short_desc_nonedit_display")[0].text
	long_desc = soup.select(".bz_first_comment")[0].select(".bz_comment_text")[0].text
	status = soup.select("#static_bug_status")[0].text
	product = soup.select("#field_container_product")[0].text
	component = soup.select("#field_container_component")[0].text
	#TODO: select only the date/time here
	created_at = soup.select("#bz_show_bug_column_2")[0].select("td")[0].text
	print(component)


	#TODO: scrape the page with the updates, need to find who marked as resolved
	#TODO: also need to get the date/time it was marked as fixed
	#TODO: handle duplicates same way as well.
	history_url = soup.select("#bz_show_bug_column_2")[0].select("td")[1].select("a")[0]['href']
	print(history_url)