import json
import re
import requests

from time import sleep


def get_issues_query(repo, state):
	""" Returns list containing all issues in the given repo with state """
	issues = []
	date = '2000-01-01'
	# Search API can only return 1000 results at a time, so need to break calls apart by time period
	while True:
		print(date)
		r = requests.get('https://api.github.com/search/issues?q=%22%22+repo:%s+type:issue+state:%s+created:>%s&sort=created&order=asc' % (repo,state,date))
		# no more issues to collect, write to file and return
		if r.json()['total_count'] == 0:
			return issues
		issues.extend(r.json()['items'])
		if 'Link' not in r.headers:
			return issues
		next_page, last_page = re.findall(r'\<(.*?)\>', r.headers['Link'])
		print(next_page)
		print(last_page)
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

def get_issue_by_id(issues, issue_id):
	""" get issue with the given issue_id """
	for issue in issues:
		if issue['id'] == issue_id:
			return isssue
	return None

def get_issue_by_title(issues, issue_title):
	""" get issue(s) with the given issue_id """
	return [issue for issue in issues if issue['title'] == issue_title]

def get_issue_by_label(issues, label_name):
	""" get all issues that are assigned the given label """ 
	return [issue for issue in issues if label_name in issue['labels']]

def get_word_freq_title(issues):
	""" get the word frequencies in the titles of issues """
	return get_word_freq(issues, 'title')

def get_word_freq_body(issues):
	""" get the word frequencies in the bodies of issues """
	return get_word_freq(issues, 'body')

def get_word_freq(issues, key):
	""" get the word frequencies in the 'key' field of issues """
	total_words = 0
	word_freqs = {}
	#TODO: find a more comprehensive list of stop words
	stop_words = ["in", "the", "or", "and", "for", "to", "not", "on", "and", "a", "of", "as", "an", "with", "when", "are", "-", "how", "from", "is", "does", "doesn't",
				  "be", "if", "can", "so", "we", "you", "i", "have", "at", "but", "this", "that", "would", "should", "by", "can't", "it", "my", "its", "there", "was",
				  "do", "use", "", "which", "some", "will", "what", "want"]
	for issue in issues:
		# remove non alphanumeric characters
		for word in issue[key].split():
			word = re.sub(r'\W+', '', word)
			if word not in stop_words:
				word_freqs[word] = word_freqs.get(word, 0) + 1
				total_words += 1
	for word in word_freqs:
		word_freqs[word] /= total_words
	return word_freqs

def get_code_in_issue(issue):
	""" Returns any (formatted) code that is present in the body of the issue """
	s = issue['body']
	ret = []
	try:
		while(True):
			# formatted code is enclosed in ``` ````
			start = s.index("```") + 3
			end = s.index("```", start )
			# any valid HTML/JavaScript should have.
			if ('{' in s[start:end+3] or '<' in s[start:end+3]):
				ret.append(s[start:end+3])
			s = s[end+3:]
	except ValueError:
		return ret

def get_num_code_lines(issue):
	""" Return the number of lines of (formatted) code in the body of an issue """
	return sum([len(s) for s in get_code_in_issue(issue)])

'''
issues = get_issues_query('nodejs/node', 'open')
with open('data/nodejs/nodejs_issues_open.json', 'w') as f:
    json.dump(issues, f, indent=4)
'''
with open('data/react/react_issues_closed.json') as f:
	    issues = json.load(f)
for issue in issues:
	print(get_code_in_issue(issue))