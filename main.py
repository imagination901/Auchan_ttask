import sys
import pickle
from tabnanny import check
from urlextract import URLExtract
import requests

def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        print('Incorrect name of the file. Perhaps you wanted to run the command as "python main.py file_to_parse.dat"?')

    extracted_data = extract_data(file_name)
    parsed_data = parse_url(extracted_data)
    checked_urls = check_url(parsed_data)

    print(checked_urls)
    

# Extracting raw strings from the given file and addind them to a list for further processing
def extract_data(filename: str) -> list:

    data = []

    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data
    except pickle.UnpicklingError:
        print(f'Unable to extract data from this file: {filename}')
        return None

# Parsing the data to find all existing URLs from the extracted data
def parse_url(data: list) -> list:

    if data is not None:
        urls = []
        url_extractor = URLExtract()

        for string in data:
            url = url_extractor.find_urls(string)
            if url:
                urls.append(url)
        
        return urls
    else:
        return None
    
# Checking the acccessibility of the parsed URLs
def check_url(parsed_list: list) -> dict:

    if parsed_list is not None:
        checked_urls = {}

        for url in parsed_list:
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
    else:
        return {} 

if __name__ == '__main__':
    main()