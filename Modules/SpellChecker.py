from typing import *
from Modules.Dictionary import *
import math
import time
import re


def symbol_mistake(first: str, second: str,) -> float:
    table = {
        'й': ['ф', 'ы', 'ц'],
        'ц': ['й', 'ф', 'в', 'у'],
        'у': ['ц', 'ы', 'в', 'а', 'к'],
        'к': ['у', 'в', 'а', 'п', 'е'],
        'е': ['к', 'а', 'п', 'р', 'н'],
        'н': ['е', 'п', 'р', 'о', 'г'],
        'г': ['н', 'р', 'о', 'л', 'ш'],
        'ш': ['г', 'о', 'л', 'д', 'щ'],
        'щ': ['ш', 'л', 'д', 'ж', 'з'],
        'з': ['х', 'э', 'ж', 'д', 'щ'],
        'х': ['з', 'ж', 'э', 'ъ'],
        'ъ': ['х', 'э'],
        'ф': ['й', 'ц', 'ы', 'я'],
        'ы': ['ф', 'ц', 'у', 'в', 'ч', 'я'],
        'в': ['ы', 'у', 'к', 'а', 'с', 'ч'],
        'а': ['в', 'к', 'е', 'п', 'м', 'с'],
        'п': ['а', 'е', 'н', 'р', 'и', 'м'],
        'р': ['п', 'н', 'г', 'о', 'т', 'и'],
        'о': ['р', 'г', 'ш', 'л', 'ь', 'т'],
        'л': ['о', 'ш', 'щ', 'д', 'б', 'ь'],
        'д': ['л', 'щ', 'з', 'ж', 'ю', 'б'],
        'ж': ['д', 'з', 'х', 'э', 'ю'],
        'э': ['ю', 'ж', 'х', 'ъ'],
        'я': ['ф', 'ы', 'ч'],
        'ч': ['я', 'ы', 'в', 'с'],
        'с': ['ч', 'в', 'а', 'м'],
        'м': ['с', 'а', 'п', 'и'],
        'и': ['м', 'п', 'р', 'т'],
        'т': ['и', 'р', 'о', 'ь'],
        'ь': ['т', 'о', 'л', 'б'],
        'б': ['ь', 'л', 'д', 'ю'],
        'ю': ['б', 'д', 'ж', 'э'],
    }
    if first in table and second in table[first]:
        return 0.5
    return 1


def translit_replace(symbol: str):
    ru = {
        'й': 'q',
        'ц': 'w',
        'у': 'e',
        'к': 'r',
        'е': 't',
        'н': 'y',
        'г': 'u',
        'ш': 'i',
        'щ': 'o',
        'з': 'p',
        'ф': 'a',
        'ы': 's',
        'в': 'd',
        'а': 'f',
        'п': 'g',
        'р': 'h',
        'о': 'j',
        'л': 'k',
        'д': 'l',
        'я': 'z',
        'ч': 'x',
        'с': 'c',
        'м': 'v',
        'и': 'b',
        'т': 'n',
        'ь': 'm',
    }
    en = {
        'q': 'й',
        'w': 'ц',
        'e': 'у',
        'r': 'к',
        't': 'е',
        'y': 'н',
        'u': 'г',
        'i': 'ш',
        'o': 'щ',
        'з': 'p',
        '[': 'х',
        ']': 'ъ',
        'a': 'ф',
        's': 'ы',
        'd': 'в',
        'f': 'а',
        'g': 'п',
        'h': 'р',
        'j': 'о',
        'k': 'л',
        'l': 'д',
        ';': 'ж',
        "'": 'э',
        'z': 'я',
        'x': 'ч',
        'c': 'с',
        'v': 'м',
        'b': 'и',
        'n': 'т',
        'm': 'ь',
        ',': 'б',
        '.': 'ю',
    }
    if symbol in en:
        return en[symbol]
    if symbol in ru:
        return ru[symbol]
    return ""


def transliterate(word: str) -> str:
    new_word = ""
    for symbol in word:
        new_word += translit_replace(symbol)
    return new_word


class Rambler:
    def __init__(self, todo: str, done: str, mistakes: float, location: TrieNode):
        self.todo = todo
        self.done = done
        self.mistakes = mistakes
        self.location = location

    def count_chance(self) -> float:
        return math.log((self.location.weight + 1) * (len(self.done) + 1)) \
               / (1 << int(self.mistakes))


class SpellChecker:
    def __init__(self, dictionary, transliterate_word=True, max_team_size=512):
        self.dictionary = dictionary
        self.transliterate_word = transliterate_word
        self.max_team_size = max_team_size
        self.max_mistake = 0

    def correct(self, word: str,) -> List[str]:
        leads = []
        leads += self._correct(word)
        if self.transliterate_word:
            leads += self._correct(transliterate(word))
        leads = sorted(leads, key=lambda x: float(x.mistakes))
        if len(leads) > 0:
            min_mistake = leads[0].mistakes
            result = set()
            for leader in leads:
                if leader.mistakes == min_mistake:
                    result.add(leader.done)
                else:
                    break
            return list(result)
        else:
            return []

    def _correct(self, word: str) -> List[Rambler]:
        self.max_mistake = len(word) // 2
        walkers = []
        leads = []
        walkers.append(Rambler(word, "", 0, self.dictionary.root))
        while len(walkers) != 0:
            next_gen = []
            for walker in walkers:
                if walker.mistakes <= self.max_mistake:
                    self._make_step(walker, next_gen, leads)
            walkers = self._remove_useful_walkers(next_gen)
        return leads

    def _make_step(self, rambler: Rambler, team: List[Rambler], finished: List[Rambler]):
        if len(rambler.todo) > 0:
            cur_rambler_symbol = rambler.todo[0]
        elif rambler.location.is_terminal:
            finished.append(rambler)
            return
        else:
            cur_rambler_symbol = ""

        todo = rambler.todo[1:] if len(cur_rambler_symbol) > 0 else ""

        for index, child in enumerate(rambler.location.children):
            if child is not None:
                char = get_symbol(index)
                if char == cur_rambler_symbol:
                    # все ОК
                    team.append(Rambler(todo,
                                        rambler.done + char,
                                        rambler.mistakes,
                                        child))
                else:
                    # замена
                    team.append(Rambler(todo,
                                        rambler.done + char,
                                        rambler.mistakes + symbol_mistake(char, cur_rambler_symbol),
                                        child))
                    # вставка
                    team.append(Rambler(rambler.todo,
                                        rambler.done + char,
                                        rambler.mistakes + 1,
                                        child))
        # удаление
        if not rambler.location.is_terminal:
            team.append(Rambler(todo,
                                rambler.done,
                                rambler.mistakes + 1,
                                rambler.location))

    def _remove_useful_walkers(self, walkers: List[Rambler]) -> List[Rambler]:
        walkers = sorted(walkers, key=lambda x: x.count_chance(), reverse=True)
        return walkers[:self.max_team_size]

    def correct_all(self, stems: List[str]) -> List[List[str]]:
        return [self.correct(w) for w in stems]

    def correct_text(self, text: str) -> List[str]:
        answer = []
        for word in re.findall("[а-яА-Яa-zA-Z]+", text):
            word = word.lower()
            answer.append(self.correct(word))
        return answer


if __name__ == "__main__":
    t = time.time()
    print("Load start")
    dictionary = Dictionary()
    print("Load end, time", time.time() - t)
    spell_checker = SpellChecker(dictionary, False)

    word = input("word: ")
    while word != "exit":
        print(spell_checker.correct(word))
        word = input("word: ")
