import os
import re
import numpy
from numpy.random import choice
from numpy.random import randint
import sys

"""
A method to read in the contents of a given file.
param input_filename: rhe name of a local file
returns: the content of that file interpreted as a string
"""
def read_corpus(input_filename):
    f_handle = open(input_filename)
    content = f_handle.read()
    f_handle.close()
    return content

"""
Generates a dictionary with words as keys and the words which come after them as values, with
each value containing in itself a count of how many times it succeeds the given key.
i.e. in the string 'Dynamic programming is cool', we would end up with the dict
{
    "Dynamic": {
        "programming":
            {"count" : 1}
    }
    "programming": {
        "is":
            {"count": 1}
    }
    "is": {
        "cool"
        {
            {"count": 1}
        }
    }
    "cool"
    {
        None
    }
}
param corpus_contents: the contents of the initial corpus
returns: a ditionary of the structure specified above
"""
def generate_dictionary(corpus_contents):
    words_arr = re.compile("[A-Za-z']+").findall(corpus_contents)
    final_dict = {}
    for i in range(0, len(words_arr) - 1):
        focus_word = words_arr[i]
        if focus_word not in final_dict:
            final_dict[words_arr[i]] = {}
        if words_arr[i + 1] not in final_dict[focus_word]:
            final_dict[focus_word][words_arr[i + 1]] = {"count":1}
        else:
            final_dict[focus_word][words_arr[i + 1]]["count"] += 1
    return final_dict

"""
Adds the probability a given word appears after its preceding word to the dictionary under the key "p".
param word_dictionary: a dictionary generated by generate_dictionary above
returns: a dictionary similar to the one above, with key "p" now added at the same level as count
"""
def add_probabilities(word_dictionary):
    for preword in word_dictionary.keys():
        total_count = 0
        for postword in word_dictionary[preword].keys():
            total_count += word_dictionary[preword][postword]["count"]
        for postword in word_dictionary[preword].keys():
            word_dictionary[preword][postword]["p"] = word_dictionary[preword][postword]["count"] / total_count
    return word_dictionary

"""
Takes the dictionary with counts and probabilities and generates a string using numpy's weighted choice
utility.
param word_dictionary: dictionary of corpus words with counts and probabilities
param starting_key: the word you want the string to start with
param length: desired length of the string
returns: a generated string
"""
def generate_chain(word_dictionary, starting_key, length):
    retstring = starting_key
    keyword = starting_key

    for i in range(0, length):
        if isinstance(keyword, numpy.ndarray):
            keyword = keyword.item(0)
        prob_dist = [word_dictionary[keyword][key]["p"] for key in word_dictionary[keyword].keys()]
        keyword = choice(list(word_dictionary[keyword].keys()), 1, prob_dist)
        retstring = retstring + " " + keyword.item(0)
    return retstring

"""
A method that takes in an input string and adds punctuation and chapter & verse numbers at randomized 
points throughout. 
param input_string: string you want to "biblify"
returns: "biblified" string
"""
def biblify(input_string):
    chapter = 1
    verse = 2

    words_arr = re.compile("[A-Za-z']+").findall(input_string)
    words_arr.insert(0, "[1:1] ")

    word_count = 0
    for i in range(0, len(words_arr) - 1):
        if words_arr[i][0].isupper():
            if word_count > randint(25, 40):
                if randint(1,3) == 2:
                    if verse >= randint(20, 30):
                        chapter += 1
                        verse = 1
                    else:
                        verse += 1
                    words_arr.insert(i, ".")
                    words_arr.insert(i + 1, "\n")
                    words_arr.insert(i + 2, "[" + str(chapter) + ":" + str(verse) + "]")
                    word_count = 0;
        word_count += 1;

    words_arr.append(".")
    ret_str = " ".join(words_arr)
    return re.sub(r'\s\.', ".", ret_str)    

def main():
    usg_str = "python markov.py [starting key phrase] [length of string] [filename]"
    if len(sys.argv) != 4:
        print(usg_str)
        return
    content = read_corpus(os.path.join(os.path.dirname(__file__),sys.argv[3]))
    dict = generate_dictionary(content)
    dict_with_probs = add_probabilities(dict)
    chain = generate_chain(dict_with_probs, sys.argv[1],int(sys.argv[2]))
    biblified_chain = biblify(chain)
    print(biblified_chain)

if __name__ == "__main__":
    main()