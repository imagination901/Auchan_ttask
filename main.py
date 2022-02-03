import sys
import pickle
from urlextract import URLExtract
import requests
from loguru import logger


def main():

    logger.add('debug.log', format="{time},{level},{message}", level="DEBUG", rotation="5 min", retention="20 min")

    try:
        file_name = sys.argv[1]
        extracted_data = extract_data(file_name)
        url_list = parse_url(extracted_data)

        while True:
            checked_urls = check_url(url_list)

            for i in checked_urls:
                print(len(i))

    except IndexError:
        logger.error("User didn't provide a filename as a command line argument.")

    except Exception as e:
        logger.error(e)


# Extracting raw strings from the given file and addind them to a list for further processing
def extract_data(filename: str) -> list:

    data = []

    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data

    except pickle.UnpicklingError:
        logger.error(f'File -{filename}- can not be unpickled.')
        return None

    except Exception as e:
        logger.error(e)
        return None


# Parsing the data to find all existing URLs from the extracted data
def parse_url(data: list) -> list:

    try:
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
    except Exception as e:
        logger.error(e)
    
# Checking the acccessibility of the parsed URLs and their endpoint addresses
def check_url(parsed_list: list) -> list[dict]:

    checked_urls = {}
    endpoint_urls = {}

    if parsed_list is not None:
        for url in parsed_list:
            try:
                response = requests.get(url[0], timeout=5)
                if response.history:
                    checked_urls[response.history[0].url] = response.history[0].status_code
                    endpoint_urls[response.history[0].url] = response.url
                else:
                    checked_urls[url[0]] = response.status_code
            except requests.exceptions.MissingSchema as SchemaError:
                logger.info(f'Schema Error, {url} is not a valid URL')
            except requests.exceptions.ConnectTimeout as TimeoutError:
                logger.info(f'Timeout Error, {url} is not responding') 
            except Exception as e:
                logger.info(f'{e}, url: {url}')

        return [checked_urls, endpoint_urls]

    else:
        return [{},{}] 

if __name__ == '__main__':
    main()