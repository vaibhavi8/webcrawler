import string
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import time
import numpy as np
import math


# Creates dictionary from list of words
def words_to_dict(li):
    new_dict = {}
    for i in li:
        if i not in new_dict:
            new_dict[i] = 1
        else:
            new_dict[i] += 1

    # Sort dictionary by ranking
    new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse = True))
    return new_dict


# Creates a list of words separated by white space
def words_to_list(words):
    # Creates a list of the words in the text with space delimiter
    word_list = words.split()
    return word_list


# Format the text by removing all punctuation and converting to lower case
def format_text(text):
    text_from_html = text.translate(str.maketrans("", "", string.punctuation))
    text_from_html = text_from_html.lower()
    return text_from_html


def create(text, repo_lang):
    # Format text: remove punctuation and lowers character case
    words = format_text(text)

    # Makes a list of words separated by white space
    word_list = words_to_list(words)

    # Builds a dictionary of words with their frequency
    word_dict = words_to_dict(word_list)

    # Builds an index of keys for the corresponding dictionary
    keys_list = list(word_dict)

    # Creates a file with 100 top words
    filename = './repository-' + repo_lang + '/frequency.txt'
    f = open(filename, 'w')
    f.write("Rank\tWord\t\t\tFrequency\n")
    for i in range(0,100):
        f.write(str(i+1) + "\t" + keys_list[i] + "\t\t\t" + str(word_dict[keys_list[i]]) + "\n")


    # Build Zipf's Law table
    zipf_data = create_zipf(word_dict, keys_list)
    #print(zipf_data)
    # Build Heap's Law table
    heap_data = create_heaps(word_list)

    create_graphs(zipf_data, heap_data)
    return


def create_zipf(dictn, keys):
    """
    Method called in order to create the Zipf's table and graph from the text
 
    Creates a sorted dictionary from the list by rank, prints the information,
    and lastly generates a graph of word rank vs frequency

    """
    # Ranks correspond to word indexes
    zipfs = list()

    for i in range(0, len(dictn)):
        zipfs.append((i,dictn[keys[i]]))

    # Zip corresponding index and frequencies of each word to create graph
    return zipfs



def create_heaps(li):
    """
    Method called in order to create the Heap's table and graph from the text

    Generates a list for Heap's law by tracking number of words (words_list) and 
    unique words in the text (set_size)

    """
    heaps = list()

    temp_dict = {}
    unique_words = 0
    set_size = 0
    for i in li:
        if i not in temp_dict:
            temp_dict[i] = 1
            unique_words += 1
            set_size += 1
        else:
            set_size += 1
        heaps.append((unique_words, set_size))

    # Create a list of the number of words and the corresponding set size, and return
    return heaps

def f(x):
    with np.errstate(divide='ignore', invalid='ignore'):
        return 1/x

def create_graphs(zipf, heap):
    first_y = zipf[0]
    first_y = first_y[1]
    x = np.array(range(0, first_y))
    y = f(x)

    plt.figure()
    plt.title('Zipf\'s Law')
    plt.plot(*zip(*zipf), label = 'actual')
    plt.plot(x, first_y*y , label='expected')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()

    plt.figure()
    plt.title('Heap\'s Law')
    plt.plot(*zip(*heap))
    plt.xlabel('Words in Collection')
    plt.ylabel('Words in Vocabulary')

    plt.show()