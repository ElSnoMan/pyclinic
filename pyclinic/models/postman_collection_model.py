from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class PostmanCollectionInfo(BaseModel):
    postman_id: str = Field(..., alias="_postman_id")
    postman_schema: str = Field(..., alias="schema")
    name: str
    description: Optional[str]


class PostmanCollection(BaseModel):
    info: PostmanCollectionInfo
    variable: Optional[List[Dict]]
    item: Optional[List[Dict]]


class PostmanRequestQuery(BaseModel):
    key: str
    value: str


class PostmanRequestUrl(BaseModel):
    raw: str
    protocol: Optional[str]
    host: List[str]
    path: List[str]
    query: Optional[List[PostmanRequestQuery]]


class PostmanRequest(BaseModel):
    method: str
    header: List[Dict]
    url: Union[PostmanRequestUrl, str]  # if POST or PUT, then url is str
    body: Optional[Dict]


class PostmanResponse(BaseModel):
    name: str
    original_request: PostmanRequest = Field(..., alias="originalRequest")
    status: str
    code: int
    header: List[Dict]
    cookie: List[Dict]
    body: Any


class PostmanItem(BaseModel):
    name: str
    event: Optional[List[Dict]]
    request: PostmanRequest
    response: List[PostmanResponse]
