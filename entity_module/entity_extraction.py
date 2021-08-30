from ncbi_module import ncbi_scrape
from wikipedia_module import wiki_query
from bing_module import bing_websearch
from bing_module import API_KEY

class source:
    def __init__(self,method):
        self.method = method
    def get_data(self,params: dict):

        if self.method == 'wikipedia':
            wiki_data = wiki_query(query_list=params["query"]).get_data(
                number_of_searches=params["number_of_searches"],
                url= params["url"],
                comments=params["comments"],
                summary=params["summary"],
                )
            return wiki_data
        if self.method == "ncbi":

            ncbi_data = ncbi_scrape(query=params["query"]).get_data(
                Official_Symbol=params["Official_Symbol"],
                Official_Full_Name=params["Official_Full_Name"],
                Primary_source=params["Primary_source"],
                See_related=params["See_related"],
                Gene_type=params ["Gene_type"],
                RefSeq_status=params["RefSeq_status"],
                Organism=params["Organism"],
                Lineage=params["Lineage"],
                Also_known_as=params["Also_known_as"],
                Expression=params["Expression"],
                Summary=params["Summary"],
                Orthologs=params["Orthologs"],
                ncbi_url=params["ncbi_url"],
                bing_query=params["bing_query"]
            )

            return ncbi_data

        if self.method =='bing':
            bing_data = bing_websearch(key=API_KEY).send_request(
                query=params["query"][0],
                count=params["number_of_searches"])
            return bing_data

