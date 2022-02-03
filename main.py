import pickle
from urlextract import URLExtract

# 1. Extracting raw strings from the given file and addind them to a list for further processing

data = []

with open("messages_to_parse.dat", 'rb') as file:
    data = pickle.load(file)