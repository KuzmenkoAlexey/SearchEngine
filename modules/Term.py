class Term:
    term = ""
    tf = 0

    def __init__(self, term, tf):
        self.term = term
        self.tf = tf

    def __str__(self):
        return "({0}, {1})".format(self.term, self.tf)
