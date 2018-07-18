class Node:
    def __init__(self, value='', left=None, center=None, right=None, parent=''):
        self.value = value
        self.left = left
        self.center = center
        self.right = right
        self.parent = parent
        self.inverse_index = []


class TernaryTree:
    def __init__(self):
        self.root = None

    def add(self, value):
        if len(value) <= 2:
            return None
        if self.root:
            self._add(value, self.root)
        else:
            self.root = Node(value[0])
            if self.root.center is not None:
                self._add_word(value, self.root.center)
            else:
                self.root.center = Node(value[1], parent=value[0])

    def _add(self, value, current_node):
        if value[0] == current_node.value:
                if current_node.center is not None:
                    self._add_word(value, current_node.center)
                else:
                    current_node.center = Node(value[1], parent=value[0])
                    self._add_word(value[1:], current_node.center)
        elif value[0] < current_node.value:
            if current_node.left is not None:
                self._add(value, current_node.left)
            else:
                current_node.left = Node(value[0])
                if current_node.left.center is not None:
                    self._add_word(value, current_node.left.center)
                else:
                    current_node.left.center = Node(value[1], parent=value[0])
                    self._add_word(value[1:], current_node.left.center)
        else:
            if current_node.right is not None:
                self._add(value, current_node.right)
            else:
                current_node.right = Node(value[0])
                if current_node.right.center is not None:
                    self._add_word(value, current_node.right.center)
                else:
                    current_node.right.center = Node(value[1], parent=value[0])
                    self._add_word(value[1:], current_node.right.center)

    def _add_word(self, value, current_node):
        if len(value) < 2:
            return
        if value[0] == current_node.value:
            if current_node.center is None:
                current_node.center = Node(value[1], parent=value[0])
                self._add_word(value[1:], current_node.center)
            else:
                self._add_word(value, current_node.center)
        else:
            if current_node.value >= value[1]:
                if current_node.left is not None:
                    self._add_word(value, current_node.left)
                else:
                    current_node.left = Node(value[1], parent=value[0])
                    self._add_word(value[1:], current_node.left)
            else:
                if current_node.right is not None:
                    self._add_word(value, current_node.right)
                else:
                    current_node.right = Node(value[1], parent=value[0])
                    self._add_word(value[1:], current_node.right)

    def search2d(self, value, it, current_node):
        if current_node.value == value[it]:
            return self.search(value, it, current_node)
        elif current_node.value > value[it]:
            if current_node.left is not None:
                return self.search2d(value, it, current_node.left)
            else:
                return None
        else:
            if current_node.right is not None:
                return self.search2d(value, it, current_node.right)
            else:
                return None

    def search(self, value, it, current_node):
        if current_node is None:
            return None
        if current_node.value == value[it] and it == len(value) - 1:
            return current_node.inverse_index
        elif current_node.value == value[it] and it != len(value) - 1:
            if current_node.center is not None:
                return self.search(value, it+1, current_node.center)
            else:
                return None
        else:
            return self.search2d(value, it, current_node)

    def add_index(self, value, index):
        if self.root is None:
            self.add(value)
        self.result = self.search(value, 0, self.root)
        if self.result is None:
            self.add(value)
        self.result = self.search(value, 0, self.root)
        if self.result is not None:
            self.result.append(index)
            self.result.sort()
