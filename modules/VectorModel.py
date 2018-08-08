import math
import pickle

from modules.PageRank import PageRank
from modules.InverseIndexTree import TernarySearchTree
from modules.TfIdfVectorModel import VectorModel, Term

pr = PageRank()
tree = TernarySearchTree()
vm = VectorModel()


class Cont:
    def __init__(self, href, terms, links):
        self.href = href
        self.terms = terms
        self.links = links


class IndexLoader:
    index = None

    def _load(self):
        with open('../data/data.pickle', 'rb') as f:
            obj = pickle.load(f)
        return obj

    def _save(self, new_data):
        with open('../data/data.pickle', 'wb') as f:
            self.pic = pickle.Pickler(f)
            self.pic.dump(new_data)


class IndexAdder(IndexLoader):
    def __init__(self):
        self.obj = []
        try:
            self.obj = self._load()
            vm.clear()
            for ob in self.obj:
                pr.add_page(ob.href, ob.links)
                vm.add(ob.href, ob.terms)
        except Exception:
            pass

    def add(self, href, terms, links=None):
        self.obj.append(Cont(href, terms, links))
        if len(self.obj) % 1 == 0:
            self._save(self.obj)
        pr.add_page(href, links)
        vm.add(href, terms)


class IndexSearcher(IndexLoader):

    def search(self, terms):
        self.obj = []
        try:
            self.obj = self._load()
            vm.clear()
            for ob in self.obj:
                pr.add_page(ob.href, ob.links)
                vm.add(ob.href, ob.terms)
        except Exception:
            pass
        pr.process()
        first_array = pr.get_ranks()
        second_array = vm.search(terms)
        result = []
        for i in range(len(first_array)):
            for j in range(len(second_array)):
                if str(first_array[i][0]) == str(second_array[j][0]):
                    result.append([first_array[i][0],
                                   math.fabs(first_array[i][1] * 0.6 + second_array[j][1] * 0.4)])
        second_result = []
        for i in range(len(second_array)):
            flag = True
            for j in range(len(result)):
                if str(second_array[i][0]) == str(result[j][0]):
                    flag = False
                    break
            if flag:
                second_array[i][1] *= 0.4
                second_result.append(math.fabs(second_array[i]))
        result.extend(second_result)
        result.sort(key=lambda x: x[1], reverse=True)
        return result
