class SignatureHash:

    def __init__(self, char_set):
        self.CHAR_SET = char_set

    def _symb_category(self, ch: chr):
        i = 0
        for ch_set in self.CHAR_SET:
            if ch in ch_set:
                return i
            i += 1
        return i

    def sig_hash(self, str_to_hash: str):
        n = 0
        for c in str_to_hash:
            i = self._symb_category(c)
            n |= 1 << i
        return n

    def _mistakes(self, numb: int):
        all_mistakes = []
        for i in range(len(self.CHAR_SET) + 1):
            if numb & (1 << i):
                mist_numb = numb - (1 << i)
            else:
                mist_numb = numb + (1 << i)
            all_mistakes.append(mist_numb)
        return all_mistakes

    def sig_hash_with_mistakes(self, str_to_hash: str):
        answer = [self.sig_hash(str_to_hash)]
        answer.extend(self._mistakes(answer[0]))
        return answer



