import pandas as pd
import string
import enchant
import sys
from pattern.en import lemma
sys.path.append('./lib')

from show_process import ShowProcess

d_GB = enchant.Dict("en_GB")
d_US = enchant.Dict("en_US")

def clean_data(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)):
            clean.append(token)

    return ' '.join(clean) + '\n'

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def clean_no_digit(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)) and not hasNumbers(token):
            clean.append(token)

    return ' '.join(clean) + '\n'

def clean_pattern(tokens):
    clean = []

    for token in tokens:
        #normalize token
        token = token.lower()
        token = token.strip(string.punctuation)

        if token != '' and (d_GB.check(token) or d_US.check(token)) and not hasNumbers(token):
            token = lemma(token)
            clean.append(token)

    return ' '.join(clean) + '\n'

if __name__ == '__main__':
    lyric_csv = './data/lyrics.csv'
    lyric_data = './data/lyrics.' + sys.argv[1]

    #read the csv file and store the lyrics in lyrics_store []
    csvReader = pd.read_csv(lyric_csv)
    csvReader = csvReader.drop(0)
    lyrics_store = csvReader['lyrics']

    #get the tokens in lyrics
    data = ''
    process = ShowProcess(len(lyrics_store))

    if sys.argv[1] == 'data':
        clean = clean_data
    elif sys.argv[1] == 'nd':
        clean = clean_nd
    else:
        clean = clean_pattern

    for line in lyrics_store:
        process.show_process()
        line = str(line)
        tokens = line.split()
        data += clean(tokens)

    with open(lyric_data, 'w+') as f:
        f.wirte(data)
