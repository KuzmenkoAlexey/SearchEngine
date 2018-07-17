from typing import *

RU_ALPHABET_LEN = ord('я') - ord('а') + 1
EN_ALPHABET_LEN = ord('z') - ord('a') + 1

node_counter = 0


def get_symbol_num(char: str) -> int:
    if ord('а') <= ord(char) <= ord('я'):
        return ord(char) - ord('а')
    elif ord('a') <= ord(char) <= ord('z'):
        return ord(char) - ord('a') + RU_ALPHABET_LEN
    else:
        raise NameError("wrong symbol")


def get_symbol(num: int) -> str:
    if num < RU_ALPHABET_LEN:
        return chr(num + ord('а'))
    elif num < RU_ALPHABET_LEN + EN_ALPHABET_LEN:
        return chr(num - RU_ALPHABET_LEN + ord('a'))
    else:
        raise NameError("wrong symbol")


class TrieNode:
    def __init__(self):
        self.weight = 0
        self.is_terminal = False
        self.children = [None] * (RU_ALPHABET_LEN + EN_ALPHABET_LEN)


class Dictionary:
    def __init__(self, filename="Data/lexicon.txt"):
        self.root = TrieNode()
        self.filename = filename
        if filename is not None:
            self.load_dictionary(filename)

    def add_word(self, word: str):
        global node_counter
        cur_node = self.root
        for symbol in word:
            try:
                symbol_num = get_symbol_num(symbol)
            except Exception:
                print("Error in Dictionary.add_word")
                return

            if cur_node.children[symbol_num] is None:
                cur_node.children[symbol_num] = TrieNode()
                node_counter += 1
            cur_node = cur_node.children[symbol_num]
            cur_node.weight += 1

        cur_node.is_terminal = True

    def find_word(self, word: str) -> bool:
        cur_node = self.root
        for symbol in word:
            try:
                symbol_num = get_symbol_num(symbol)
            except Exception:
                print("Error in Dictionary.find_word")
                return False
            if cur_node.children[symbol_num] is None:
                return False
            cur_node = cur_node.children[symbol_num]
        if cur_node.is_terminal:
            return True
        return False

    def load_dictionary(self, filename):
        file = open(filename, 'r')
        for word in file:
            self.add_word(word.strip().replace('-', ""))
        file.close()

    def update_dictionary(self):
        if self.filename is None:
            raise NameError("No dictionary filename")
        words = []
        self.get_words(self.root, "", words)
        file = open(self.filename, 'w')
        for word in words:
            file.write(word + '\n')
        file.close()

    def get_words(self, node: TrieNode, word: str, lexicon: List[str]):
        if node.is_terminal:
            lexicon.append(word)
        for index, elem in enumerate(node.children):
            if elem is not None:
                char = get_symbol(index)
                self.get_words(elem, word + char, lexicon)


if __name__ == '__main__':
    d = Dictionary("lexicon.txt")
    d.update_dictionary()

# d.add_word("hello")
# d.add_word("hell")
# d.add_word("првивет")
# d.add_word("elijah")
# d.update_dictionary()
# d = Dictionary(filename="lexicon.txt")
# print(node_counter)
# while True:
#     word = input("Enter word: ")
#     print(d.find_word(word))
#     print()

