from modules.SignatureHash import SignatureHash
import math, pickle


class HashIndex:
    file = 'data/hashindex.pkl'
    pic = None

    class RowDocument:
        def __init__(self, doc_id, term, parent_row):
            self.doc_id = doc_id
            self.term = term
            self.parent = parent_row

    class RowDocumentCollection:
        def __init__(self, parent_hash_table):
            self.docs = []
            self.parent_hash_table = parent_hash_table
            self.doc_id = 0

        def add(self, row_doc):
            if len(self.docs) == 0:
                self.doc_id = row_doc.doc_id
            self.docs.append(row_doc)

        def rsv(self):
            k = 1.2
            b = 0.75
            res = 0
            for doc in self.docs:
                N = len(self.parent_hash_table.hrefs)
                dft = doc.parent.df
                tfd = doc.term.tf
                idf = math.log(N / dft)
                idf = idf if idf > 0 else 0
                Lave = self.parent_hash_table._l_average()
                Ld = self.parent_hash_table.hrefs[doc.doc_id][1]
                res += idf * ((1 + k) * tfd / (k * ((1 - b) + b * (Ld / Lave)) + tfd))
            return res

    class IndexRow:
        def __init__(self):
            self.docs = []
            self.df = 0

        def add(self, doc_id, term):
            self.docs.append(HashIndex.RowDocument(doc_id, term, self))
            self.df += 1

        def save(self):
            HashIndex.pic.dump(self.df)
            HashIndex.pic.dump(self.docs)
            for i in range(len(self.docs)):
                HashIndex.pic.dump(self.docs[i])

        def load(self):
            self.df = HashIndex.pic.load()
            self.docs = HashIndex.pic.load()
            for i in range(len(self.docs)):
                self.docs[i] = HashIndex.pic.load()

        def __str__(self):
            res = "idf: {0}; ( ".format(self.df)
            for doc in self.docs:
                res += "({0}, {1}), ".format(doc.term, doc.doc_id)
            res += ")"
            return res

    FIRST_CHAR_SET = ['бп', 'вф', 'эеё', 'сз', 'ня', 'дт',
                      'хг', 'шщ', 'ъьы', 'ий', 'оа', 'ую', 'цч', 'мр', 'жк', '.,!?']

    hrefs = []

    def __init__(self):
        self.sig_hash = SignatureHash(self.FIRST_CHAR_SET)
        self.counter = 0
        try:
            self.load()
        except Exception as e:
            print(e)
            self.hash_table = [HashIndex.IndexRow() for _ in range(2 ** (len(self.FIRST_CHAR_SET) + 2))]

    def add(self, href, terms, links=None):
        doc_id = len(self.hrefs)
        words = 0
        for term in terms:
            term_hash = self.sig_hash.sig_hash(term.term)
            self.hash_table[term_hash].add(doc_id, term)
            words += term.tf
        self.hrefs.append((href, words))
        self.counter += 1

        if self.counter > 10:
            self.counter = 0
            self.save()

    def search(self, terms, with_mistakes=False):
        doc_lists = []
        for term in terms:
            if with_mistakes:
                term_hashes = self.sig_hash.sig_hash_with_mistakes(term)
                row_list = []
                for term_hash in term_hashes:

                    for doc in self.hash_table[term_hash].docs:
                        row_doc_col = HashIndex.RowDocumentCollection(self)
                        row_doc_col.add(doc)
                        row_list.append(row_doc_col)
                doc_lists.append(row_list)
            else:
                term_hash = self.sig_hash.sig_hash(term)
                row_list = []
                for doc in self.hash_table[term_hash].docs:
                    row_doc_col = HashIndex.RowDocumentCollection(self)
                    row_doc_col.add(doc)
                    row_list.append(row_doc_col)
                doc_lists.append(row_list)
        if len(doc_lists) == 0:
            return None

        while len(doc_lists) > 1:
            l1 = doc_lists[len(doc_lists) - 1]
            l2 = doc_lists[len(doc_lists) - 2]
            doc_lists.pop()
            doc_lists.pop()
            doc_lists.append(self._merge(l1, l2))

        result_list = []
        if len(doc_lists[0]):
            i = 0
            while i < len(doc_lists[0]) - 1:
                if doc_lists[0][i].doc_id == doc_lists[0][i + 1].doc_id:
                    doc_lists[0][i].docs.extend(doc_lists[0][i + 1].docs)
                    doc_lists[0].pop(i + 1)
                else:
                    i += 1
        for doc in doc_lists[0]:
            result_list.append((self.hrefs[doc.doc_id][0], doc.rsv()))
        result_list.sort(key=lambda x: x[1])
        result_list.reverse()
        return result_list

    @staticmethod
    def _merge(row_list_col1, row_list_col2):
        i1 = i2 = 0
        res_list = []
        while i1 < len(row_list_col1) and i2 < len(row_list_col2):
            doc1 = row_list_col1[i1]
            doc2 = row_list_col2[i2]
            if doc1.doc_id == doc2.doc_id:
                res_list.append(doc1)
                for doc in doc2.docs:
                    doc1.add(doc)
                i1 += 1
                i2 += 1
            elif doc1.doc_id < doc2.doc_id:
                i1 += 1
            else:
                i2 += 1
        return res_list

    def save(self):
        f = open(self.file, 'wb')
        HashIndex.pic = pickle.Pickler(f)
        HashIndex.pic.dump(self.hrefs)
        HashIndex.pic.dump(self.hash_table)
        for i in range(len(self.hash_table)):
            if self.hash_table[i]:
                self.hash_table[i].save()
        f.close()

    def load(self):
        f = open(self.file, 'rb')
        HashIndex.pic = pickle.Unpickler(f)
        self.hrefs = HashIndex.pic.load()
        self.hash_table = HashIndex.pic.load()
        for i in range(len(self.hash_table)):
            if self.hash_table[i]:
                self.hash_table[i].load()
        f.close()

    def _l_average(self):
        L = 0
        for href in self.hrefs:
            L += href[1]
        return L / len(self.hrefs)

    def __sizeof__(self):
        return self.hash_table.__sizeof__()

    def __str__(self):
        res = ""
        for i in range(len(self.hash_table)):
            if len(self.hash_table[i].docs) != 0:
                res += "{0}, ({1})\n".format(i, self.hash_table[i])
        return res