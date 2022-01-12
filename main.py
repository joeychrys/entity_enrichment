import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Optional
from entity_module import source

import uvicorn

test = "acetyl-coa carboxylase alpha"
app = FastAPI()
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "test")
    correct_password = secrets.compare_digest(credentials.password, "1234")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get('/wikipedia/{query}/')
def read_item(
    username: str = Depends(get_current_username),
    query: str=None,
    number_of_searches: Optional[int]=1,
    url: Optional[bool] = True,
    summary: Optional[bool] = True,
    comments: Optional[bool] = True,
):

# this is a patch for ncbi because it currently does not accept a list
  
    params = {
        "query": [query],
        "number_of_searches":number_of_searches,
        "url": url,
        "summary": summary,
        "comments": comments
    }

    entity_data = source("wikipedia").get_data(params)
    return entity_data, {"username": username}

@app.get('/ncbi/{query}/')
def read_item(
    username: str = Depends(get_current_username),
    query: str=None,
    Official_Symbol: Optional[bool]= True,
    Official_Full_Name: Optional[bool]= True,
    Primary_source: Optional[bool]= True,
    See_related: Optional[bool]= True,
    Gene_type: Optional[bool]= True,
    RefSeq_status: Optional[bool]= True,
    Organism: Optional[bool]= True,
    Lineage: Optional[bool]= True,
    Also_known_as: Optional[bool] = True,
    Expression: Optional[bool] = True,
    Summary: Optional[bool]= True,
    Orthologs: Optional[bool] = True,
    ncbi_url: Optional[bool]= True,
    bing_query: Optional[bool] = True,
):

    params = {
        "query": query,
        "Official_Symbol": Official_Symbol,
        "Official_Full_Name": Official_Full_Name,
        "Primary_source": Primary_source,
        "See_related": See_related,
        "Gene_type": Gene_type,
        "RefSeq_status": RefSeq_status,
        "Organism": Organism,
        "Lineage": Lineage,
        "Also_known_as": Also_known_as,
        "Expression": Expression,
        "Summary":Summary,
        "Orthologs": Orthologs,
        "ncbi_url": ncbi_url,
        "bing_query": bing_query

    }

    entity_data = source("ncbi").get_data(params)
    return entity_data, {"username": username}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
