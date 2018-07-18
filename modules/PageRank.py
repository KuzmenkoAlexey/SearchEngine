import re
import numpy as np


class LinkProcessor:
    def link_processor(self, link):
        return re.search(r'[0-9]+', link).group()


class Page(LinkProcessor):
    def __init__(self, href, links):
        self.name = int(self.link_processor(href))
        self.childs = list(map(int, map(self.link_processor, links)))


class PageRank:
    def __init__(self, d=0.85):
        self.index = {}
        self.back_index = {}
        self.pages = []
        self.unique = set()
        self.d = d

    def add_page(self, href, links):
        self.pages.append(Page(href, links))

    def unique_count(self):
        for el in self.pages:
            self.unique.add(el.name)
            for link in el.childs:
                self.unique.add(link)

    def indexing_set(self):
        i = 0
        for el in list(self.unique):
            self.index[el] = i
            self.back_index[i] = el
            i += 1

    def fill_matrix(self):
        self.matrix = [[0 for _ in range(len(self.index))] for _ in range(len(self.index))]
        self.multiplier = [[self.d] for _ in range(len(self.index))]
        size = 0
        for el in self.pages:
            links = list(set(el.childs))
            size = len(links)
            if size != 0:
                value = 1 / size
            else:
                value = 0
            for i in range(size):
                self.matrix[self.index[el.name]][self.index[links[i]]] = value
        # self.transpose_matrix()
        # for _ in range(size):
        #     self.mul()
        self.matrix = np.array(self.matrix).transpose()
        self.multiplier = np.array(self.multiplier)

        for _ in range(size):
            new_matrix = self.matrix.dot(self.multiplier)
            self.multiplier = new_matrix

    def rank(self):
        self.ranks = [[self.back_index[i], float(self.multiplier[i])] for i in range(len(self.multiplier))]
        self.ranks.sort(key=lambda x: x[1], reverse=True)

    def get_ranks(self):
        return self.ranks

    def normalize_index(self):
        for i in range(len(self.ranks)):
            self.index[self.ranks[i][0]] = i
            self.back_index[i] = self.ranks[i][0]

    def process(self):
        self.unique_count()
        self.indexing_set()
        self.fill_matrix()
        self.rank()
        self.normalize_index()
