__author__ = 'ROHIT'

import enchant
import nltk
import re
from math import sqrt

from nltk.corpus import stopwords

porter = nltk.PorterStemmer()
dictionary = enchant.Dict("en_US")
def main():
    f1 = open("Files/set_1.txt", "r")
    f2 = open("Files/set_2.txt", "r")
    content1 = f1.read()
    content2 = f2.read()
    f1.close()  # closing file
    f2.close()
    content1 = re.split('\. | |\n|\.|\'|\(|\)|\"|\?|\,|!| -|-', content1)  # splitting file
    content2 = re.split('\. | |\n|\.|\'|\(|\)|\"|\?|\,|!| -|-', content2)
    content1_true = wordList(content1)
    content2_true = wordList(content2)
    f1 = open("Files/true1.txt","w")
    f2 = open("Files/true2.txt","w")
    for x in content1_true:
        f1.write(x + "-" + str(content1_true[x]) + "\n")

    for x in content2_true:
        f2.write(x + "-" + str(content2_true[x]) + "\n")
    f1.close()
    f2.close()
    print cosine(content1_true,content2_true)

def wordList(content):
    index = 0
    temp = []
    for x in content:
        #print x
        if len(x) < 3 or x in stopwords.words("english"):
            pass
        else:
            #print x
            stemword = porter.stem(x)
            if dictionary.check(stemword):
                temp.insert(index, stemword)  #poopulating temp with stemmed words
            else:
                temp.insert(index, x)
            index += 1

    content = temp
    #for x in temp:
    #    print x
    true = {}
    false = {}

    for x in content:
        if dictionary.check(x):
            if x in true:
                true[x] += 1
            else:
                true[x] = 1
        else:
            if x in false:
                false[x] += 1
            else:
                false[x] = 1

    for x in false:
        templist = dictionary.suggest(x)
        for y in templist:
            if y in true:
                true[y] = true[y] + false[x]
                false[x] = 0
                break

    for x in false:
        if false[x] != 0:
            true[x] = false[x]

    #for x in true:
    #    print x + "-" + str(true[x])

    return true

def cosine(dict1,dict2):
    sum = 0
    mod1 = 0
    mod2 = 0
    #print str(len(dict1)) + " " + str(len(dict2))
    for x in dict1:
        mod1 = mod1 + dict1[x]*dict1[x]

    for x in dict2:
        mod2 = mod2 + dict2[x]*dict2[x]

    mod1 = sqrt(mod1)
    mod2 = sqrt(mod2)
    #print mod1
    #print mod2

    if len(dict1) > len(dict2):
        (dict1,dict2) = (dict2,dict1)
    #print str(len(dict1)) + " " + str(len(dict2))
    for x in dict1:
        if x in dict2:
           # print x + " " + str(dict1[x]) + " " + str(dict2[x])
            sum = sum + dict1[x]*dict2[x]
    result = sum / (mod1 * mod2)
    return  result
    # mod will be very high for a large file so the cosine value decreases. though there is a similarity due to large file
    # i.e due to high mod value

if __name__ == "__main__":
    main()


    # d = enchant.Dict("en_US")
    # print d.check("Hello")