import math
from modules import InverseIndexTree as tree
from modules.PageRank import LinkProcessor


class Term(LinkProcessor):
    def __init__(self, href, term, times):
        self.href = int(self.link_processor(href))
        self.term = term
        self.times = times
        self.tf = None
        self.idf = None
        self.tf_idf = None


class VectorModel(LinkProcessor):
    def __init__(self):
        self.documents = dict()
        self.root = tree.TernaryTree()

    def add(self, href, terms):
        href = self.link_processor(str(href))
        self.documents[href] = terms
        words_in_doc = 0
        for el in terms:
            self.root.add_index(el.term, href)
            words_in_doc += el.times
        for el in terms:
            self.count_tf(el, words_in_doc)

    def count_tf(self, element, words_in_doc):
        element.tf = (element.times / words_in_doc)

    def search(self, terms):
        for term in terms:
            self.count_tf(term, len(terms))

        docs = set()
        answer = {}
        for term in terms:
            result = self.root.search(term.term, 0, self.root.root)
            if result is not None:
                term.idf = math.log10(len(self.documents) / len(result))
                for el in result:
                    docs.add(el)
            else:
                term.idf = 0
        for doc in docs:
            answer[doc] = list()
            for el in self.documents[doc]:
                for term in terms:
                    if el.term == term.term:
                        el.tf_idf = el.tf * term.idf
                        answer[doc].append(el)
        ranks = []
        for doc in docs:
            sample = 0
            for el in answer[doc]:
                for term in terms:
                    if term.term == el.term:
                        sample += el.tf_idf
            ranks.append([doc, sample])
        ranks.sort(key=lambda x: x[1])
        return ranks
