# required imports 
from bing_module import bing_websearch
from bing_module import API_KEY
import pandas as pd 
from bs4 import BeautifulSoup
import requests 
import json as j

class ncbi_scrape:
    def __init__(self, query, method: str='bing'):
        r'''
        NCBI Scrapper
        ~~~~~~~~~~~~

        This Scrapes NCBI for gene summery data. The current endpoint 
        is 'https://www.ncbi.nlm.nih.gov/gene'. The query is first sent to 
        the Bing API. The Bing API then sends a list of urls. The most 
        relevent URL is then passed to be webscraped and formated to 
        JSON.

        ----------
        Parameters:
            * query: (str) Required to send a request to the Bing API.
            * method: (str) Determines whether or not to use the Bing 
            API. If set to 'manual', then the full url must be passed as the query
                - 'bing' (default)
                - 'manual'
        '''
        self.query = query
        self.method = method 
        self.site_filter = ' site:https://www.ncbi.nlm.nih.gov/gene'
        self.query_and_site_filter = self.query + self.site_filter

    def get_urls(self):

        # adding "site:" makes sure that bing targets a certain type of site
        bing_json_response = bing_websearch(key=API_KEY).send_request(query=self.query_and_site_filter,count=1)

        urls = []
        for i in bing_json_response['webPages']['value']:
            url_dict = {
                'urls' : i['displayUrl'],
            }
            urls.append(url_dict)
        return urls

    def get_data(
        self, 
        Official_Symbol: bool= True,
        Official_Full_Name: bool= True,
        Primary_source: bool= True,
        See_related: bool= True,
        Gene_type: bool= True,
        RefSeq_status: bool= True,
        Organism: bool= True,
        Lineage: bool= True,
        Also_known_as: bool = True,
        Expression: bool = True,
        Summary: bool= True,
        Orthologs: bool = True,
        ncbi_url: bool= True,
        bing_query: bool = True,
        return_df: bool= False,
        save_json: bool= False,
        json_file_name: str='ncbi_data.json',
        ):
        
        # parse JSON from Bing websearch API
        if self.method =='bing':
            urls = self.get_urls()
            url = urls[0]['urls']
        if self.method =='manual':
            url = self.query

        # get site's html and parse it
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        summery_data = soup.find_all('dl',{'id':'summaryDl'})

        # create a list of ids
        id_column = []
        for item in summery_data[0].find_all('dt'):
            id_column.append(item.text)

        # create a list of attributes
        atter_column = []
        for item in summery_data[0].find_all('dd'):
            atter_column.append(item.text)

        # clean up the strings in the list 
        try:
            id_column = [i.replace('\n','').lstrip(' ').rstrip(' ') for i in id_column]
            id_column = [i.replace('                        ','') for i in id_column]
            
            atter_column = [i.replace('\n',' ').lstrip(' ').rstrip(' ') for i in atter_column]
            atter_column = [i.replace('provided by RGD','') for i in atter_column]
            atter_column = [i.replace('provided by HGNC','') for i in atter_column]
            atter_column = [i.replace('provided by MGI','') for i in atter_column]
            atter_column = [i.replace(' See more','') for i in atter_column]
            atter_column = [i.replace(' all','') for i in atter_column]

        except:
            pass

        # create dataframe
        df = pd.DataFrame()
        df['Id'] = id_column
        df['Attribute'] = atter_column

        # make the id column the table header
        df = df.T
        df.columns = df.iloc[0]
        df = df.drop('Id').reset_index(drop=True)

        # remove the 'NEW' column
        try:
            df = df.drop(columns={'NEW'})
        except:
            pass

        # add url to the response
        df["url"] = url
        df["bing_query"] = self.query_and_site_filter

        # drop columns based on data wanted
        try:
            if Official_Symbol == False:
                df = df.drop(columns="Official Symbol")
            if Official_Full_Name == False:
                df = df.drop(columns="Official Full Name")
            if Primary_source == False:
                df = df.drop(columns="Primary source")
            if See_related == False:
                df = df.drop(columns="See related")
            if Gene_type == False:
                df = df.drop(columns="Gene type")
            if RefSeq_status == False:
                df = df.drop(columns="RefSeq status")
            if Organism == False:
                df = df.drop(columns="Organism")
            if Lineage == False:
                df = df.drop(columns="Lineage")
            if Also_known_as == False:
                df = df.drop(columns="Also known as")
            if Summary == False:
                df = df.drop(columns='Summary')
            if Expression == False:
                df = df.drop(columns="Expression")
            if Orthologs == False: 
                df = df.drop(columns="Orthologs")
            if ncbi_url == False:
                df = df.drop(columns='url')
            if bing_query == False:
                df = df.drop(columns="bing_query")
        except:
            pass

        # return a Dataframe if specified
        if return_df == True:
            return df

        # save the JSON response to a File if specified
        if save_json == True:
            df = df.to_dict(orient="dict")
            dict_response = {}
            dict_response['source'] = "NCBI"
            dict_response['response'] = [{
                "query": self.query,
            }]
            dict_response['response'][0]["data"] = df

            with open(json_file_name, 'w') as outfile:
                j.dump(dict_response,outfile)
            return j.dumps(dict_response,indent=4)

        # return dict for API 
        else:
            df = df.to_dict(orient="dict")
            dict_response = {}
            dict_response['source'] = "NCBI"
            dict_response['response'] = [{
                "query": self.query,
            }]
            dict_response['response'][0]["data"] = df 
            return dict_response

            

