import requests
import json

class bing_websearch:
    def __init__(self, key):
        r'''
        Bing Websearch API
        ~~~~~~~~~~~~

        This wrapper easily sends a request to the Bing WebSearch API and receives
        a JSON response in the terminal or to a JSON file.

        ----------
        Parameters:
            * key: (str) Required to send a request to the API. 
        '''
        self.key = key
        self.endpoint = 'https://bingwebsearchapi.cognitiveservices.azure.com' + "/bing/v7.0/search"
 

    def send_request(
        self,
        query: str='Bing Search API',
        filter: str='Webpages', 
        count: int=3,
        mkt: str='en-US',
        save_to_file: bool=False,
        file_name: str='bing_data'):
        r"""
        This method constructs the request that will be sent to the Bing API.

        ----------
        Parameters:
            * query: (str) The user's search query term. The term may not be empty.
            * filter: (str) A comma-delimited list of answers to include in the response.
                - Computation
                - Entities
                - Images
                - News
                - RelatedSearches
                - SpellSuggestions
                - TimeZone
                - Videos
                - Webpages
            * count: (int) The number of search results to return in the response.
            * mkt: (str) The market where the results come from. 
                Typically, mkt is the country where the user is making the request from.
            * save_to_file: (bool) Whether or not to save the JSON response to a JSON file.
            * file_name: (str) File name of JSON response.

        Returns:
            * JSON 
        """

        # create params dict 
        params = {
            'q': query,
            'mkt': mkt,
            'count': count,
            'responseFilter': filter
        }

        # header that handles the key
        headers = {
            'Ocp-Apim-Subscription-Key': self.key
        }

        try:
            # sends the request 
            response = requests.get(self.endpoint, headers=headers, params=params)

            # error handling
            response.raise_for_status()

            headers = response.headers
            data = response.json()

            # create a json file with the response
            if save_to_file == True:
                jsonString = json.dumps(data)
                jsonFile = open(f"{file_name}.json", "w")
                jsonFile.write(jsonString)
                jsonFile.close()

        except Exception as ex:
            raise ex
        
        return data
