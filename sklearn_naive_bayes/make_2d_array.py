from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import csv, string

IGNORE_WORDS = stopwords.words('english')

ALL_CATEGORIES = [
    'Action',
    'Community',
    'Information',
]


def read_csv_file(file_name):
    """
    Returns the contents of the csv file as an array
    """
    csv_contents = []
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            csv_contents.append(row)
    return csv_contents


def remove_punctuation_and_lowercase(strn):
    """
    Removes the punctuation from the string
    and lowercases it.
    """
    char_list = []
    backslash_found = False
    for char in strn:
        if backslash_found:
            backslash_found = False
            if char == 'n':
                char_list.append(' ')
        elif not char in string.punctuation:
            char_list.append(char)
        elif char == '\\':
            backslash_found = True
    word_list = ((''.join(char_list)).lower()).split(' ')

    return [word for word in word_list if word != '' and word not in IGNORE_WORDS]


def make_2d_arrays(index_dict, all_messages, func):
    """
    Takes an index dictionary and all the messages and create 2d arrays of 0s and 1s
    where each 1 means that value in the index dictionary was found in that message.

    If func is None, each unique word is used.  Otherwise, func is called on the word
    to get the values for that word
    """
    all_message_array = []
    for messages in all_messages:
        message_array = []
        for message in messages:
            curr_appender = [0]*len(index_dict)
            if func is None:
                lst = message
            else:
                lst = func(message)
            for value in lst:
                curr_appender[index_dict[value]] = 1
            message_array.append(curr_appender)
        all_message_array.append(message_array)

    return all_message_array


def make_index_dict(unique_words, func):
    """
    Creates the index dictionary based on the unique words and the passsed function.

    If func is None, then each word gets an index
    Otherwise, func is called on the word (ex: to get the synonym sets of a word) and each
    value in the return of func(word) is given an index
    """
    index_dict = {}
    index = 0
    for word in unique_words:
        if func is None:
            if word not in index_dict: # This check should not be necessary, but just to be safe
                index_dict[word] = index
                index += 1
        else:
            for value in func(word):
                if value not in index_dict:
                    index_dict[value] = index
                    index += 1
    
    return index_dict


def make_message_arrays(unique_words, all_messages, func):
    """
    Creates the list of 2d arrays based on the given words, messages, and
    desired function
    """
    index_dict = make_index_dict(unique_words, func)
    return make_2d_arrays(index_dict, all_messages, func)


def make_messages(csv_files):
    """
    Reads the csv files and stores all the words in the messages
    """
    unique_words = set()
    all_messages = []
    all_categories = []

    for csv_file in csv_files:
        contents = read_csv_file(csv_file)
        messages = []
        categories = []
        for value in contents:
            message = value[1]
            words = []
            for word in remove_punctuation_and_lowercase(message):
                unique_words.add(word)
                words.append(word)

            messages.append(words)
            category = ALL_CATEGORIES.index(value[0])
            categories.append(category)

        all_messages.append(messages)
        all_categories.append(categories)

    return unique_words, all_messages, all_categories


def driver(csv_files):
    """
    Driver for make_2d_array.py
    """
    unique_words, messages, categories = make_messages(csv_files)
    return make_message_arrays(unique_words, messages, None), categories