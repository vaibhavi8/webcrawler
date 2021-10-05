import string
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup


def create(text):
    words = format_text(text)
    word_list = words_to_list(words)

    # Initialize an empty list to track the frequencies of each
    # word in the word list for Zipf's
    word_freq = []

    # Initialize an empty set to track the unique words in the text
    # and a list to track the set size for each word in Heap's
    word_set = set()
    set_size = []

    # Loop through all the words in the list and create lists for
    # Zipf's and Heap's
    for word in word_list:
        word_freq.append(word_list.count(word))
        word_set.add(word)
        set_size.append(len(word_set))

    zipf_data = create_zipf(word_list, word_freq)
    heap_data = create_heaps(word_list, set_size)
    create_graphs(zipf_data, heap_data)
    return


def create_zipf(word_list, word_freq):
    """
    Method called in order to create the Zipf's table and graph from the text
 
    Creates a sorted dictionary from the list by rank, prints the information,
    and lastly generates a graph of word rank vs frequency

    """
    totalWords = len(word_list)

    sorted_dict = create_sorted_dictionary(word_list, word_freq)

    zipf_table = generate_zipf_table(sorted_dict, totalWords)

    print_zipf(zipf_table)

    # Ranks correspond to word indexes
    zipf_ranks = list(range(1, len(zipf_table) + 1))

    # Create a list of each word's frequency
    zipf_frequency = list(item[1] for index, item in enumerate(sorted_dict, start=1))

    # Zip corresponding index and frequencies of each word to create graph
    return list(zip(zipf_ranks, zipf_frequency))


def create_heaps(word_list, set_size):
    """
    Method called in order to create the Heap's table and graph from the text

    Generates a list for Heap's law by tracking number of words (words_list) and 
    unique words in the text (set_size)

    """
    # Create a list of numbers from 1 to the total number of words
    number_of_words_list = list(range(1, len(word_list) + 1))

    # Create a list of the number of words and the corresponding set size, and return
    return list(zip(number_of_words_list, set_size))


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


def create_sorted_dictionary(word_list, word_freq):
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


def create_graphs(zipf, heap):
    plt.figure()
    plt.title('Zipf\'s Law')
    plt.plot(*zip(*zipf))
    plt.xlabel('Rank')
    plt.ylabel('Frequency')

    plt.figure()
    plt.title('Heap\'s Law')
    plt.plot(*zip(*heap))
    plt.xlabel('Words in Collection')
    plt.ylabel('Words in Vocabulary')

    plt.show()
