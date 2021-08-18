from News import *
from Retriver import *
from score import score

All_News = []
equalizer = Equalizer(dictionary)
# read the News file
with open('IR_Spring2021_ph12_7k.csv', encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    for row in csv_reader:
        if line != 0:
            n = News(row[0], row[1], row[2], equalizer)
            All_News.append(n)
            c = n.tokenizee_content
            d = n.abc()
            # n.short_form(c)
        line += 1
dictionary.remove_k_frequent_words(50)
equalizer.equalize_dict()
dictionary1 = equalizer.ret_dict()
dictionary.sort_dict()
score_giver = score(dictionary)
score_giver.cal_tf()
score_giver.cal_idf()
score_giver.cal_tfidf()
dictionary.create_doc_vectors()
dictionary.create_champions_list()
dictionary.save_dict()
ret = Retriever(dictionary)
ret.get_query()
ret.retrieve('champ')

