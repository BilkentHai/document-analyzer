import requests
import re
import html2text
import math

# TF RELATED
def process_document(URL):
	# setup
	s = requests.session()
	s.headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'}

	# get document in html form 
	response = s.get(URL)
	raw_text = response.text

	# convert html to text
	document = html2text.html2text(raw_text).encode('utf-8')
	return document

def generate_term_count_dict(document):
	# seperate terms into list
	terms_list = re.findall(b"[a-zA-Z]+", document)

	# record term counts in a dictionary
	term_count_dict = {}
	for term in terms_list:
		if len(term) >= 2:
			term = term.lower()
			if term in term_count_dict:
				term_count_dict[term] += 1
			else:
				term_count_dict[term] = 1

	return term_count_dict

def sum_values_in_dict(dict):
	sum = 0

	for key, value in dict.items():
		sum = sum + value

	return sum

def calculate_tf(term_count, num_of_terms):
	return term_count / num_of_terms

# tf is specific to document for each word
def generate_term_tf_dict(term_count_dict):
	num_of_terms = sum_values_in_dict(term_count_dict)
	term_tf_dict = {}

	for key, value in term_count_dict.items():
		term_tf_dict[key] = calculate_tf(value, float(num_of_terms))

	return term_tf_dict

# IDF RELATED
def generate_set_of_all_terms(URL_termcountdict_dict):
	terms_set = []

	for URL, term_count_dict in URL_termcountdict_dict.items():
		for term, count in term_count_dict.items():
			if term not in terms_set:
				terms_set.append(term)

	return terms_set

def calculate_idf(num_of_docs_containing_term, num_of_docs):
	return math.log(num_of_docs / float(num_of_docs_containing_term))

# idf is general to all documents for each word
def generate_term_idf_dict(terms_set, URL_termcountdict_dict):
	num_of_docs = len(URL_termcountdict_dict)
	term_idf_dict = {}

	for term in terms_set:
		containing_doc_count = 0
		for URL, dictionary in URL_termcountdict_dict.items():
			if term in dictionary:
				containing_doc_count += 1

		term_idf_dict[term] = calculate_idf(containing_doc_count, num_of_docs)

	return term_idf_dict


def get_tfidf_scores(URLs):
	# save count of each term for each URL
	URL_termcountdict_dict = {}
	# save tf of each term for each URL
	URL_termtfdict_dict = {}

	for URL in URLs:
		doc = process_document(URL)
		term_count_dict = generate_term_count_dict(doc)
		term_tf_dict = generate_term_tf_dict(term_count_dict)

		URL_termcountdict_dict[URL] = term_count_dict
		URL_termtfdict_dict[URL] = term_tf_dict

	terms_set = generate_set_of_all_terms(URL_termcountdict_dict)
	term_idf_dict = generate_term_idf_dict(terms_set, URL_termcountdict_dict)

	term_tfidf_dict = {}
	for URL in URLs:
		for term in terms_set:
			if term in URL_termcountdict_dict[URL]: # check if term exists in URL
				if term in term_tfidf_dict:
					term_tfidf_dict[term] += URL_termtfdict_dict[URL][term] * term_idf_dict[term]
				else:
					term_tfidf_dict[term] = URL_termtfdict_dict[URL][term] * term_idf_dict[term]
	print(term_tfidf_dict)
	return term_tfidf_dict