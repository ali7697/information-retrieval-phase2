import math
from copy import deepcopy
import heapq
from Equalizer import *
from score import *


class Retriever:
    query: str

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.equalizer = Equalizer(self.dictionary)

    def get_dict(self):
        self.dictionary.dictionary, self.dictionary.id_to_url_dict, self.dictionary.doc_vectors, \
            self.dictionary.champions_list_dict = self.dictionary.read_dict()

    def get_query(self):
        self.query = input('Please enter the query: ')

    def get_equalized_query(self):
        alphabet = 'آاأبپتثجچحخدذرزژسشصضطظعغفقکكگلم‌نوؤهیيئء'  # نیم فاصله داره
        r = re.compile(f'[{alphabet}]+')
        words = r.findall(self.query)
        words = self.equalizer.equalize_query(words)
        return words

    def retrieve(self, champ_or_normal, with_heap_or_without_heap):
        words = self.get_equalized_query()
        doc_similarity_dict_not_for_all_docs = self.cal_cosine_similarity(words, champ_or_normal)
        if with_heap_or_without_heap == 'without_heap':
            # using heap instead of this
            largest = [[k, v] for k, v in sorted(
                doc_similarity_dict_not_for_all_docs.items(), key=lambda item: item[1],  reverse=True)]
        else:
            largest = heapq.nlargest(10, list(doc_similarity_dict_not_for_all_docs.items()), key=lambda x: x[1])
        largest = sorted(largest, key=lambda x: x[1], reverse=True)[0:40]
        output_printed = dict()
        # print('Num of docs: ' + str(len(doc_similarity_dict_not_for_all_docs.keys())))
        for pair in largest:
            output_printed[pair[0]] = self.dictionary.id_to_url_dict[pair[0]]
            print(str(pair[0]) + '\t' + output_printed[pair[0]])
        return output_printed

    def cal_cosine_similarity(self, words, champ_or_normal):
        # vector of the query
        query_vector = dict()
        for word in words:
            if word not in query_vector.keys():
                weight_of_word = 1 + math.log10(words.count(word))
                query_vector[word] = weight_of_word
        # calculate cosine similarity
        doc_similarity_dict = dict()
        if champ_or_normal == 'champ':
            used_dict = deepcopy(self.dictionary.champions_list_dict)
        else:
            used_dict = deepcopy(self.dictionary.dictionary)
        for word in query_vector.keys():
            for i in range(1, len(used_dict[word])):
                doc_id = used_dict[word][i][0]
                weight = used_dict[word][i][1]
                if doc_id in doc_similarity_dict.keys():
                    doc_similarity_dict[doc_id] = doc_similarity_dict[doc_id] + \
                                                  (query_vector[word] * weight) / self.dictionary.doc_vectors[doc_id]
                else:
                    doc_similarity_dict[doc_id] = (query_vector[word] * weight) / self.dictionary.doc_vectors[
                        doc_id]  # 0 doc id 1 weight
        return doc_similarity_dict
