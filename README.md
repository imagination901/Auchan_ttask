# URL unpickler and parser

- threading and multiprocessing wasn't used as per the specific requirement to utilize reqests module. Official requests documentation recommends using grequests module as requests is not designed for async. This might be subject to further enhancement of this script. 

- the script timing is 126.87987470626831. This includes several URL timeout exceptions and nested redirects. There's a room for improvement here with grequests/asyncio and/or better requests timeout configuration.  

- Final len() of the keys in output dicts are 67 and 58.
