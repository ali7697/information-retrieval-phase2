from Retriver import *
from Dictionary import *
from score import *
import time

dictionary = Dictionary()
dictionary.dictionary, dictionary.id_to_url_dict, dictionary.doc_vectors, dictionary.champions_list_dict = dictionary.read_dict()
print(len(dictionary.dictionary.keys()))
ret = Retriever(dictionary)
ret.get_query()
t1 = time.time()
ret.retrieve('cha', 'without_heap')
t2 = time.time()
print(t2-t1)
