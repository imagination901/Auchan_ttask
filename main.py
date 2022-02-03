import pickle
from urlextract import URLExtract

# 1. Extracting raw strings from the given file and addind them to a list for further processing

data = []

with open("messages_to_parse.dat", 'rb') as file:
    data = pickle.load(file)


# 2. Parsing the data to find all existing URLs from the extracted data

urls = []
url_extractor = URLExtract()

for string in data:
    url = url_extractor.find_urls(string)
    if url:
        urls.append(url)

for i, url in enumerate(urls):
    print(i, url)