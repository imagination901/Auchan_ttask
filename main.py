import pickle
from tabnanny import check
from urlextract import URLExtract
import requests

# 1. Extracting raw strings from the given file and addind them to a list for further processing

def extract_data() -> list:

    data = []

    with open('messages_to_parse.dat', 'rb') as file:
        data = pickle.load(file)

    return data


# 2. Parsing the data to find all existing URLs from the extracted data

def url_parser() -> list:

    urls = []
    url_extractor = URLExtract()

    for string in extract_data():
        url = url_extractor.find_urls(string)
        if url:
            urls.append(url)
    
    return urls
    

# 3. Checking the acccessibility of the parsed URLs

def url_checker() -> dict:

    checked_urls = {}

    for url in url_parser():
        try:
            x = requests.head(url[0], timeout=5)
            checked_urls[url[0]] = x.status_code
        except requests.exceptions.MissingSchema as SchemaError:
            print(url, 'SchemaError: This is not a valid URL address.')
        except requests.exceptions.ConnectTimeout as TimeoutError:
            print(url, 'TimeoutError: Server is not responding') 
        except Exception as e:
            print('Some other error occured: ' + e)
    
    return checked_urls

print(url_checker())
            