import string
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup


def create_zipf(text):
    """
    Method called in order to create the zipf's table and graph from the text

    Formats the text by removing puncuations, adds all the words into a list, 
    creates a sorted dictionary from the list by rank, prints the information,
    and lastly generates a graph of word rank vs frequency

    """

    words = format_text(text)

    word_list = words_to_list(words)
    totalWords = len(word_list)

    sorted_dict = create_sorted_dictionary(word_list)

    zipf_table = generate_zipf_table(sorted_dict, totalWords)

    print_zipf(zipf_table)

    # Ranks correspond to word indexes
    zipf_ranks = list(range(1, len(zipf_table) + 1))

    # Create a list of each word's frequency
    zipf_frequency = list(item[1] for index, item in enumerate(sorted_dict, start = 1))

    # Zip corresponding index and frequencies of each word to create graph
    zipf_rank_frequency = list(zip(zipf_ranks, zipf_frequency))
    create_graph(zipf_rank_frequency)
    
    return

def create_heaps(text):
    """
    Method called in order to create the zipf's table and graph from the text

    Formats the text by removing puncuations, adds all the words into a list, 
    and generates a list for Heap's law by tracking number of words and 
    unique words in the text

    """
    words = format_text(text)
    word_list = words_to_list(words)
    heaps_table = generate_heaps(word_list)
    create_graph(heaps_table)
    return

def format_text(text):
    # Parses through the html to only extract the words
    text_from_html = BeautifulSoup(text, features="html.parser").text

    # Format the text by removing all punctuation and converting to lower case
    text_from_html = text_from_html.translate(str.maketrans("", "", string.punctuation))
    text_from_html = text_from_html.lower()
    return text_from_html

def words_to_list(words):
    # Creates a list of the words in the text with space delimiter
    word_list = words.split()
    return word_list

def create_sorted_dictionary(word_list):
    word_freq = []

    # For each word in the word list, add the frequency of that word
    # to the word_freq list
    for word in word_list:
        word_freq.append(word_list.count(word))

    # Zip together the words and their frequencies in a dictionary, making each pair only
    # appear once
    word_dict = dict(list(zip(word_list, word_freq)))

    # Sort the dictionary by their frequency and return
    sorted_dict = sorted(word_dict.items(), key=lambda item: item[1], reverse=True)
    return sorted_dict

def generate_zipf_table(sorted_dict, total_words):
    zipf_table = []

    # For each word in the sorted dictionary, calculate the probabilty
    # and probabilty of occurance
    for index, item in enumerate(sorted_dict, start=1):
        probability = item[1] / total_words
        probability_of_occurance = probability * index

        # Append the information for each word in the table and return
        zipf_table.append({"word": item[0],
                            "frequency": item[1],
                            "rank": index,
                            "probability": probability,
                            "probability_of_occurance": probability_of_occurance})
    return zipf_table

def print_zipf(zipf_table):
    # Print each word's info in a specific format
    format_string = "|{:12}|{:12.0f}|{:>12}|{:12.2f}|{:12.2f}|"

    for index, item in enumerate(zipf_table, start=1):
        print(format_string.format(item["word"],
                                    item["frequency"],
                                    item["rank"],
                                    item["probability"],
                                    item["probability_of_occurance"]))
    return

def generate_heaps(word_list):

    # Initialize an empty set to track the unique words in the text
    # and a list to trank the set size for each word
    word_set = set()
    set_size = []

    # For each word in the list, add the word in the set of unique words
    # and append the size of this set to the set_size list for each word
    for word in word_list:
        word_set.add(word)
        set_size.append(len(word_set))
    
    # Create a list of numbers from 1 to the total number of words
    number_of_words_list = list(range(1, len(word_list) + 1))

    # Create a list of the number of words and the corresponding set size, and return
    heaps_list = list(zip(number_of_words_list, set_size))
    return heaps_list

def create_graph(table):
    """
    Takes a zipped list of x values and y values to plot and generate the graph

    Zipf's: word rank vs frequency
    Heap's: words in collection vs words in vocabulary
    """
    plt.plot(*zip(*table))
    plt.show()
