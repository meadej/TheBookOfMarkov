import os
import re
import numpy
from numpy.random import choice

def read_corpus(input_filename):
    f_handle = open(input_filename)
    content = f_handle.read()
    f_handle.close()
    return content

def generate_dictionary(corpus_contents):
    words_arr = re.compile("[A-Za-z']+").findall(corpus_contents)
    final_dict = {}
    for i in range(0, len(words_arr) - 1):
        focus_word = words_arr[i]
        if focus_word not in final_dict:
            final_dict[words_arr[i]] = {}
        elif words_arr[i + 1] not in final_dict[focus_word]:
            final_dict[focus_word][words_arr[i + 1]] = {"count":1}
        else:
            final_dict[focus_word][words_arr[i + 1]]["count"] += 1
    return final_dict

def add_probabilities(word_dictionary):
    for preword in word_dictionary.keys():
        total_count = 0
        for postword in word_dictionary[preword].keys():
            total_count += word_dictionary[preword][postword]["count"]
        for postword in word_dictionary[preword].keys():
            word_dictionary[preword][postword]["p"] = word_dictionary[preword][postword]["count"] / total_count
    return word_dictionary

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


def main():
    content = read_corpus(os.path.join(os.path.dirname(__file__),"corpus/holybible.txt"))
    dict = generate_dictionary(content)
    dict_with_probs = add_probabilities(dict)
    print(generate_chain(dict_with_probs, "And", 25))

if __name__ == "__main__":
    main()