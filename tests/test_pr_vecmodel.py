from modules.main import *

index_searcher = IndexSearcher()
index_adder = IndexAdder()


index_adder.add('https://habr.com/company/pixonic/blog/417441/',
                [Term('авито', 0.5),
                 Term('яндекс', 0.5),
                 Term('момент', 0.5),
                 Term('ты', 0.5)],
                ['https://habr.com/post/417446/',
                 'https://habr.com/post/417444/',
                 'https://habr.com/post/417445/'])


result = index_searcher.search(['собакие'])
for el in result:
    print('https://habr.com/post/{}/    K: {}'.format(el[0], el[1]))

'''
1. add index - index_adder.add('https://habr.com/post/417443/', [Term('1', 'смартфон', 1),
                                Term('1', 'программирование', 1),
                                Term('1', 'блокчейн', 4),
                                Term('1', 'яндекс', 63),
                                Term('1', 'фото', 2),
                                Term('1', 'карты', 2)], 
                                ['https://habr.com/post/417446/',
                                'https://habr.com/post/417444/',
                                'https://habr.com/post/417445/'])
I - url of site that is indexing
II - terms that this site has(nothing, word, the number of this word in the text)
III - links that this site has


2. search index - result = index_searcher.search([Term('1', 'смартфон', 1),
                                Term('1', 'программирование', 1),
                                Term('1', 'блокчейн', 4),
                                Term('1', 'яндекс', 63),
                                Term('1', 'фото', 2),
                                Term('1', 'карты', 2)])
                                

I - terms that this site has(nothing, word, the number of this word in the text)
'''
