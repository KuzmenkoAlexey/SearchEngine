class TernarySearchTree():

    def __init__(self, value=None, index=None, endOfWord=False):
        self.value = value
        self.left = None
        self.right = None
        self.equal = None
        self.endOfWord = endOfWord
        self.inverse_index = []
        if self.endOfWord:
            self.inverse_index.append(index)

    def __contains__(self, word):
        node = self
        for char in word:
            while True:
                if not node:
                    return False
                if char > node.value:
                    node = node.right
                elif char < node.value:
                    node = node.left
                else:
                    last = node
                    node = node.equal
                    break
        return last.inverse_index

    def insert(self, word, index):
        char = word[0]
        if not self.value:
            self.value = char

        if char < self.value:
            if not self.left:
                self.left = TernarySearchTree()
            self.left.insert(word, index)
        elif char > self.value:
            if not self.right:
                self.right = TernarySearchTree()
            self.right.insert(word, index)
        else:
            if len(word) == 1:
                self.endOfWord = True
                self.inverse_index.append(index)
                return

            if not self.equal:
                self.equal = TernarySearchTree()
            self.equal.insert(word[1:], index)
