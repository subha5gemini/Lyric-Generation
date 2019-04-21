import pandas as pd
import numpy as np
from collections import OrderedDict, Counter
from sklearn.preprocessing import normalize
from word_index_dict import clean

lyric_data = '../data/lyrics.csv'
word_dict_file = '../data/word_index_dict'
bigram_prob = '../data/bigram_prob'
START = '<s>'
END = '</s>'

class OrderedCounter(Counter, OrderedDict):
    pass

#read the csv file and store the lyrics in lyrics_store []
csvReader = pd.read_csv(lyric_data)
csvReader = csvReader.drop(0)
lyrics_store = csvReader['lyrics']

#get the tokens in lyrics
with open(word_dict_file, 'r') as f:
    word_index_dict = eval(f.read())

counts = np.zeros((len(word_index_dict), len(word_index_dict)), dtype = float)

for line in lyrics_store:
    line = str(line)
    tokens = clean(line.split())
    previous = END

    for token in reversed(tokens):
        counts[word_index_dict[previous]][word_index_dict[token]] += 1
        previous = token

    counts[word_index_dict[previous]][word_index_dict[START]] += 1

probs = normalize(counts, norm='l1')

with open(bigram_prob, 'w+') as f:
    f.write(str(probs))
