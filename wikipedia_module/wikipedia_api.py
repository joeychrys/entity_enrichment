import wikipedia as wp
import pandas as pd
import json 

class wiki_query:
    def __init__(self, query_list):
        r'''
        Wikipedia Query
        ~~~~~~~~~~~~

        This takes a list of queries that will be sent to the Wikipedia Search API.

        ----------
        Parameters:
            * query_list: (list) Takes a list of queries and suggests Wikipedia pages. 
        '''
        self.query_list = query_list

# I first use the Wikipedia Search to give recommendations
# from the list of queries I pass into the Class

    def create_search_list(self, query, number_of_searches):
        return wp.search(query,results=number_of_searches)

# I then create a DataFrame that contains the Query and the its 
# corresponding search results

    def get_search(self, number_of_searches):
        a = []
        for query in self.query_list:
            search = {
                'query': query,
                'search_result': self.create_search_list(query,number_of_searches),
            }
            a.append(search)
        
        df = pd.DataFrame(a)
        df = df.explode(column='search_result')
        df = df.reset_index().drop(columns={'index'})
        return df

# I take this DataFrame of Queries and Search results and iterate
# over the Searches and grab the urls, descriptions, and 
# any other requested data.

    def get_data(
            self,
            number_of_searches, 
            url:        bool= True, 
            summary:    bool= True, 
            comments:   bool= True,
            return_df:  bool= False,
            save_json: bool= False,
            json_file_name: str='wiki_data.json',
        ):
        r"""
        This method returns either a dataframe or JSON string with information related to
        the search results from the list of queries.

        ----------
        Parameters:
            * number_of_searches: (int) Number of search results per query.
            * url: (bool) Url assosiated with the search result.
            * summery: (bool) Page summery assosciated with the search result.
            * comments: (bool) Errors that may arise with the the page.
            * json: (bool) Determines if the data is returned as JSON. If not true, data is returned as a dataframe.

        Returns:
            * Dict (Default)
            * Dataframe (for Testing)
            * JSON file (for Testing)
        """
        df = self.get_search(number_of_searches=number_of_searches)
        a = []
        for i in df['search_result']:
            try:
                page = wp.page(i)
            except wp.exceptions.PageError:
                warning = 'not avaliable'
            except wp.exceptions.DisambiguationError:
                warning = 'disambiguation'
            except Exception:
                warning = 'error'
            else:
                warning = 'ok'

            result = {
                'search_result': i,
                'url': page.url,
                'summary': page.summary,
                'comments': warning
            }
            a.append(result)
        df_2 = pd.DataFrame(a)
        df = pd.merge(df,df_2, on='search_result')
        df = df.drop(columns='query')

        if url == False:
            df = df.drop(columns='url')
        if summary == False:
            df = df.drop(columns='summary')
        if comments == False:
            df = df.drop(columns='comments')
        if return_df == True:
            return df
        if save_json == True:
            df = df.to_dict(orient="dict")
            dict_response = {}
            dict_response['source'] = "Wikipedia"
            dict_response['response'] = [{
                "query": self.query_list,
            }]
            dict_response['response'][0]["data"] = df

            with open(json_file_name, 'w') as outfile:
                json.dump(dict_response,outfile)
            return json.dumps(dict_response,indent=4)
        else:
            df = df.to_dict(orient='records')
            dict_response = {}
            dict_response['source'] = "Wikipedia"
            dict_response['response'] = [{
                "query": self.query_list,
            }]
            dict_response['response'][0]["data"] = df
            return dict_response

# The final result is a DataFrame
