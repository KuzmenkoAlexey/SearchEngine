from flask import *
from SearchServer.settings import *

from Modules.HashIndex import *
from Modules.Dictionary import *
from Modules.Stemmer import *
from Modules.SpellChecker import *

print("Start load dictionary")
dictionary = Dictionary()
print("Dictionary loaded")
stemmer = Stemmer(dictionary=dictionary)
spell_checker = SpellChecker(dictionary=dictionary)
print("Built index")
hash_index = HashIndex()
print("Index is ready to use")


app = Flask(__name__)
app.secret_key = '1'


@app.route('/', methods=['POST', 'GET'])
def hello_world():

    if 'query' in request.form and request.form['query'].strip() != "":
        query = request.form['query']
        terms = stemmer.get_all_stems(query)
        print(terms)
        result = hash_index.search(terms)
        all_correct = True
        for word in terms:
            all_correct = all_correct and dictionary.find_word(word)
        print("All words are correct: ", all_correct)
        #
        # if all_correct:
        #     corrected = None
        # else:
        #     corrected = spell_checker.correct_text(request.form['query'])
        #     if len(corrected) > 0:
        #         try:
        #             corrected = " ".join(corrected)
        #         except Exception:
        #             corrected = None
        #     else:
        #         corrected = None
        return render_template('index.html', docs=result, query=query, corrected=None)
    return render_template('index.html', docs=[], query="", corrected=None)


if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)
