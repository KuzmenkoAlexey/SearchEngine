import os
import sys
os.chdir('../')
sys.path.append(os.path.dirname('..'))

from flask import *
from searchServer.settings import *

from modules.HashIndex import *
from modules.Dictionary import *
from modules.Stemmer import *
from modules.SpellChecker import *

print("Start load dictionary")
dictionary = Dictionary()
print("Dictionary loaded")
stemmer = Stemmer(dictionary=dictionary)
spell_checker = SpellChecker(dictionary=dictionary)
print("Built index")
hash_index = HashIndex()
print("Index is ready to use")


app = Flask(__name__, template_folder='searchServer/templates')
app.secret_key = '1'


def brute_force(corrected: List[List[str]]) -> List[str]:
    res = []
    for variants in corrected:
        if len(res) == 0:
            res += variants
        else:
            cur_res = []
            for variant in variants:
                for cur in res:
                    cur_res.append(cur + " " + variant)
            res = cur_res
    return res


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print()
    if 'query' in request.form and request.form['query'].strip() != "":
        query = request.form['query']
        terms = stemmer.get_all_stems(query)
        try:

            print("Terms in query: ", terms)
            result = hash_index.search(terms)
            all_correct = True
            for word in terms:
                all_correct = all_correct and dictionary.find_word(word)
            print("All words are correct: ", all_correct)
            variants = None
            if not all_correct and SPELL_CHECKER:
                corrected = []
                words = get_all_words(query)
                for index, word in enumerate(terms):
                    if dictionary.find_word(word):
                        corrected.append([word])
                    else:
                        corrected.append(spell_checker.correct(words[index]))
                print("Corrected version: ", corrected)
                variants = brute_force(corrected)

            return render_template('index.html', docs=result, query=query, variants=variants,
                                   round=round)
        except UnicodeEncodeError:
            print("Warning: raised UnicodeEncodeError")

    return render_template('index.html', docs=[], query="", variants=None, round=round)


if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)
