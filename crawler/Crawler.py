import os
import sys
os.chdir('../')
sys.path.append(os.path.dirname('..'))

import requests
import time
from bs4 import BeautifulSoup

from modules.SpellChecker import *
from modules.Stemmer import Stemmer, get_all_words
from modules.Dictionary import *
from modules.Term import *
# from modules.HashIndex import HashIndex, Term
from modules.VectorModel import IndexAdder, Term
from crawler.settings import *


def update_all():
    print("Update dictionary")
    t = time.time()
    dictionary.update_dictionary()
    print("time: ", time.time() - t)

    print("Save result to file")
    t = time.time()
    if MODE == 'SH':
        search_index.save()
    print("time: ", time.time() - t)

    print("Num of pages: ", page_counter)


def get_term_list(text: str) -> List[Term]:
    words_dict = {}
    for word in get_all_words(text):
        word = word.lower()
        word = stemmer.get_stem(word)
        if word not in words_dict:
            words_dict[word] = 1
        else:
            words_dict[word] += 1
    term_list = []
    for key, value in words_dict.items():
        term_list.append(Term(key, value))
    return term_list


def get_link_list(post):
    link_list = []
    links = post.findAll('a')
    for link in links:
        if 'href' in link.attrs:
            if re.match("https://habr\.com/.+", link.attrs['href']):
                link_list.append(link.attrs['href'])
    return link_list

print("Start load dictionary")
start_time = time.time()
dictionary = Dictionary()
stemmer = Stemmer(dictionary, add_new_words=True)
spell_checker = SpellChecker(dictionary)
search_index = IndexAdder()
print("Dictionary load time: ", time.time() - start_time)

page_counter = 0
index = 0

while page_counter < MAX_PAGE_COUNTER:
    start_indexing = time.time()
    index += STEP
    time.sleep(CRAWL_DELAY)
    full_url = URL_BASE + str(START_PAGE_INDEX + index)
    res = requests.get(full_url)

    soup = BeautifulSoup(res.text, 'html5lib')
    page_counter += 1
    try:
        post = soup.find('div', {'class': "post__text"})
        text = soup.title.string + "".join(post.findAll(text=True))

        search_index.add(full_url, get_term_list(text), get_link_list(post))
        print("indexing: ", full_url)
        print("time: ", time.time() - start_indexing)
        if page_counter % 10 == 0:
            update_all()
    except AttributeError:
        page_counter -=1
        print("not exist: ", full_url)
        continue

update_all()
print("All time: ", time.time() - start_time)


