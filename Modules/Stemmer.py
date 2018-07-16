from typing import *
from Modules.Porter import Porter
from Modules.Dictionary import *
import re
import time


class Stemmer:
    def __init__(self, dictionary, add_new_words=False):
        self.porter = Porter()
        self.dictionary = dictionary
        self.add_new_words = add_new_words

    def get_stem(self, word: str) -> str or None:
        if self.dictionary.find_word(word):
            return word
        porter_result = self.porter.stem(word)
        cur_node = self.dictionary.root
        for symbol in porter_result:
            try:
                symbol_num = get_symbol_num(symbol)
            except Exception:
                print("Error in Dictionary.find_word")
                return None
            if cur_node.children[symbol_num] is None:
                if self.add_new_words:
                    self.dictionary.add_word(porter_result)
                return porter_result
            cur_node = cur_node.children[symbol_num]

        if cur_node.is_terminal:
            return porter_result

        queue = []
        queue.append((cur_node, ""))
        while len(queue) > 0:
            cur_node, ending = queue.pop(0)
            if cur_node.is_terminal:
                return porter_result + ending
            for index, elem in enumerate(cur_node.children):
                if elem is not None:
                    queue.append((elem, ending + get_symbol(index)))
        return porter_result

    def get_all_stems(self, text: str) -> List[str]:
        answer = []
        for word in re.findall("[а-яА-Яa-zA-Z]+", text):
            word = word.lower()
            answer.append(self.get_stem(word))
        return answer


if __name__ == "__main__":
    t = time.time()
    print("Load start")
    dictionary = Dictionary()
    print("Load end, time", time.time() - t)
    stemmer = Stemmer(dictionary)
    porter = Porter()

    word = input("word: ")
    while word != "exit":
        print("porter: ", porter.stem(word))
        print("stemmer: ", stemmer.get_stem(word))
        word = input("word: ")
