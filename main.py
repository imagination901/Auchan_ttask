import os
import sys
import pickle
from urlextract import URLExtract
import requests
from loguru import logger


def main():
    # Initializing the logger instance with required rotation and retention variables
    logger.add('debug.log', format="{time},{level},{message}", 
               level="DEBUG", rotation="5 min", retention="20 min")

    try:
        file_name = sys.argv[1] # Checking for the filename to parse
        extracted_data = extract_data(file_name) # Unpickling data from the file
        url_list = parse_url(extracted_data) # Parsing the data for the URLs

        # Main loop to check the URLs, status codes and URL redirects
        while True:
            checked_urls = check_url(url_list)

            for i in checked_urls: # The len of output dicts
                print(len(i))

    except IndexError:
        logger.error("User didn't provide a filename as a command line argument.")

    except Exception as e:
        logger.error(e)


def extract_data(filename: str) -> list[str]:
    """ Unpickles raw strings from the given file and addind them to a list for further processing.

    Parameters:
    filename (str): the name of the file one would like to unpickle.

    Returns:
    list[str]: returns list of strings.
    """

    data = []
    if os.path.exists(f'./{filename}'):
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
            return data

        except pickle.UnpicklingError:
            logger.error(f'File -{filename}- can not be unpickled.')
            sys.exit(1)

        except Exception as e:
            logger.error(e)
            sys.exit(1)
    else:
        logger.error(f'File path "./{filename}" does not exist. Please check the spelling')
        sys.exit(1)


def parse_url(data: list[str]) -> list:
    """ Parses the input data to find all existing URLs.

    Parameters:
    data (list[str]): list of strings to find URLs in.

    Returns:
    list: returns list of curated individual URLs.
    """
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
    
# Function to check the acccessibility of the parsed URLs and their endpoint addresses
def check_url(parsed_list: list) -> list[dict]:
    """ Checks the accessibility of URLs, their HTTP response codes, 
        and their endpoint URL addresses after nested redirects.

    Parameters:
    parsed_list(list): list containigs individual URLs as strings.

    Returns:
    list[dict]: returns a list of dicts. 
                dict0[url: str] = status_code: int, 
                dict1[original_url: str] = final_url_after_redirect: str
    """
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
